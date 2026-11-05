FROM docker:cli AS dockercli

FROM python:3.12-slim

COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker

RUN docker --version

RUN pip install --no-cache-dir flask ansible-core

WORKDIR /app

COPY app.py /app/app.py

EXPOSE 5000

CMD ["python", "app.py"]
