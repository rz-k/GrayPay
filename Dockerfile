FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
