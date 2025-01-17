FROM python:3.8-slim

COPY . /app
WORKDIR /app

RUN pip install requests

ENTRYPOINT ["python", "/app/entrypoint.py"]
