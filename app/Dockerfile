FROM python:3

WORKDIR /app

COPY . /app

RUN pip install flask prometheus_flask_exporter jaeger-client

ENV HTTP_PORT 8081

CMD [ "python", "app.py" ]
