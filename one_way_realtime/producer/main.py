import os
import time
import psycopg2
import json
from kafka import KafkaProducer

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
KAFKA_BOOTSTRAP_SERVERS = os.environ['KAFKA_BOOTSTRAP_SERVERS']
TOPIC = 'item-changes'

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def fetch_changes(conn, last_id):
    with conn.cursor() as cur:
        cur.execute("SELECT id, item_id, name, updated_at FROM item_changes WHERE id > %s ORDER BY id ASC", (last_id,))
        rows = cur.fetchall()
        return rows

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    conn = get_connection()
    last_id = 0

    while True:
        rows = fetch_changes(conn, last_id)
        for row in rows:
            id_, item_id, name, updated_at = row
            data = {"item_id": item_id, "name": name, "updated_at": str(updated_at)}
            producer.send(TOPIC, value=data)
            print(f"[Producer] Sent: {data}")
            last_id = id_
        time.sleep(2)

if __name__ == '__main__':
    main()
