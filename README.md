\# Self-Healing Infrastructure using Prometheus, Ansible and Docker



\## Project Overview



This project implements an automated self-healing infrastructure that detects NGINX service failures, generates alerts, and automatically restores the failed service using Ansible and Docker.



The solution integrates Prometheus, Blackbox Exporter, Alertmanager, a Python Flask webhook receiver, Ansible, Docker and Grafana.



The primary objective is to reduce manual intervention and demonstrate automated infrastructure monitoring, failure detection and recovery.



\## Architecture



NGINX → Blackbox Exporter → Prometheus → Alertmanager → Flask Webhook → Ansible → Docker Restart



Grafana provides monitoring dashboards and visualization.



\## Technologies Used



\- Docker and Docker Compose

\- Prometheus

\- Blackbox Exporter

\- Alertmanager

\- Ansible

\- Python and Flask

\- Grafana

\- NGINX

\- PowerShell



\## Project Features



\### 1. Infrastructure Monitoring

Prometheus continuously monitors infrastructure metrics and evaluates alert rules.



\### 2. HTTP Health Monitoring

Blackbox Exporter performs HTTP health checks against the NGINX service.



\### 3. Automated Alert Detection

Prometheus generates an NginxDown alert when the HTTP probe fails for the configured duration.



\### 4. Alert Management

Alertmanager receives Prometheus alerts and forwards actionable notifications to the Flask webhook.



\### 5. Automated Recovery

The Flask application receives failure notifications and executes an Ansible playbook.



Ansible communicates with Docker to restart the failed NGINX container.



\### 6. Monitoring Dashboard

Grafana visualizes:

\- NGINX Availability

\- NGINX Response Time

\- Monitoring Target Health

\- NGINX Failure Alerts

\- Blackbox HTTP Health Monitoring



\## Project Structure



text self-healing-infrastructure/ │ ├── alertmanager/ │   └── alertmanager.yml │ ├── ansible/ │   └── recovery.yml │ ├── blackbox/ │   └── blackbox.yml │ ├── grafana/ │   └── provisioning/ │       └── datasources/ │           └── prometheus.yml │ ├── prometheus/ │   ├── prometheus.yml │   └── alerts.yml │ ├── recovery/ │   ├── app.py │   └── Dockerfile │ ├── screenshots/ │ ├── docker-compose.yml └── README.md 



\## How Self-Healing Works



1\. Blackbox Exporter checks the NGINX HTTP endpoint.

2\. Prometheus collects the probe results.

3\. If NGINX becomes unavailable, the probe returns a failure.

4\. Prometheus evaluates the NginxDown alert rule.

5\. Alertmanager forwards the firing alert to the Flask webhook.

6\. Flask validates the alert and executes the Ansible playbook.

7\. Ansible restarts the NGINX Docker container.

8\. Blackbox Exporter checks NGINX again.

9\. Prometheus detects that the service is available.



A 60-second cooldown prevents repeated recovery attempts from being triggered too frequently.



\## Installation and Setup



\### Prerequisites



\- Docker Desktop

\- Docker Compose

\- Windows 11 or a compatible Linux environment

\- PowerShell (for the commands below)



\### Clone the Repository



bash git clone YOUR\_GITHUB\_REPOSITORY\_URL cd self-healing-infrastructure 



Replace YOUR\_GITHUB\_REPOSITORY\_URL with your actual GitHub repository URL.



\### Start the Infrastructure



bash docker compose up -d --build 



\### Check Running Containers



bash docker compose ps 



\### Access Services



| Service | URL |

|---|---|

| Grafana | http://localhost:3000 |

| Prometheus | http://localhost:9090 |

| Alertmanager | http://localhost:9093 |

| Blackbox Exporter | http://localhost:9115 |

| NGINX | http://localhost:62708 |



Grafana's default initial credentials are commonly admin/admin unless changed during setup.



\## Failure Simulation and Testing



The following test was successfully performed.



\### Step 1: Stop NGINX



bash docker stop nginx 



\### Step 2: Wait for Prometheus Detection



Prometheus detects the failed HTTP probe and triggers the configured alert after the alert duration.



\### Step 3: Alertmanager Notification



Alertmanager forwards the firing alert to the Flask recovery service.



\### Step 4: Automated Ansible Recovery



The Flask webhook executes:



bash ansible-playbook -i localhost, -c local /ansible/recovery.yml 



\### Step 5: Verify Recovery



bash docker ps --filter "name=nginx" 



The NGINX container should be running again.



\### Test Result



The complete automatic recovery workflow was successfully tested.



The recovery logs showed:



\- NGINX failure detected.

\- Ansible recovery playbook executed.

\- Docker restart task completed.

\- Ansible play recap: failed=0.

\- Self-healing successful.



\## Learning Outcomes



This project demonstrates practical experience with:



\- Infrastructure monitoring and observability.

\- Prometheus metrics and alert rules.

\- HTTP health checks using Blackbox Exporter.

\- Alertmanager webhook integration.

\- Python Flask API development.

\- Ansible automation and playbooks.

\- Docker container management.

\- Automated service recovery.

\- Grafana dashboard configuration.

\- Troubleshooting distributed containerized services.



\## Security and Production Considerations



This is a portfolio demonstration, not a production-hardened deployment.



The recovery container uses the Docker socket to restart containers. Access to this socket provides powerful control over the Docker host and must be carefully restricted in production.



A production implementation should also include authentication, access controls, secure webhook communication, persistent monitoring data, and a production-ready Flask application server.



\## Author



Bhovan Verma



Aspiring DevOps / Cloud Engineer

