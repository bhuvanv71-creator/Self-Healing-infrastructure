from flask import Flask, request, jsonify
import subprocess
import threading
import time

app = Flask(__name__)

recovery_lock = threading.Lock()
last_recovery = 0
COOLDOWN = 60


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "recovery service running"})


@app.route("/alert", methods=["POST"])
def alert():
    global last_recovery

    data = request.get_json(silent=True) or {}
    alerts = data.get("alerts", [])

    nginx_alert = any(
        item.get("labels", {}).get("alertname") == "NginxDown"
        and item.get("status") == "firing"
        for item in alerts
    )

    if not nginx_alert:
        print("IGNORED: No actionable NGINX alert", flush=True)
        return jsonify({"message": "No actionable NGINX alert"}), 200

    with recovery_lock:

        if time.time() - last_recovery < COOLDOWN:
            print("IGNORED: Recovery cooldown active", flush=True)
            return jsonify({"message": "Recovery cooldown active"}), 200

        try:
            print("NGINX FAILURE DETECTED - STARTING RECOVERY", flush=True)

            result = subprocess.run(
                [
                    "ansible-playbook",
                    "-i",
                    "localhost,",
                    "-c",
                    "local",
                    "/ansible/recovery.yml"
                ],
                capture_output=True,
                text=True,
                timeout=60
            )

            print(result.stdout, flush=True)

            if result.returncode == 0:
                last_recovery = time.time()
                print("SELF-HEALING SUCCESSFUL", flush=True)

                return jsonify({
                    "status": "success",
                    "message": "NGINX recovery completed"
                }), 200

            print("ANSIBLE RECOVERY FAILED", flush=True)
            print(result.stderr, flush=True)

            return jsonify({
                "status": "failed",
                "error": result.stderr
            }), 500

        except Exception as error:
            print("RECOVERY ERROR:", str(error), flush=True)

            return jsonify({
                "status": "error",
                "message": str(error)
            }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)