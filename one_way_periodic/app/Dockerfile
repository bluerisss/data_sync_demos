FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron
WORKDIR /app
COPY . /app
RUN pip install psycopg2-binary
RUN crontab /app/cronjob
