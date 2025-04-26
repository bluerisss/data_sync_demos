FROM python:3.10-slim
WORKDIR /app
COPY main.py .
RUN pip install psycopg2-binary
CMD ["python", "main.py"]
