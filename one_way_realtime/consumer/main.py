import os
import json
import psycopg2
from kafka import KafkaConsumer

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

def insert_item(conn, item):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO items (id, name, updated_at) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, updated_at = EXCLUDED.updated_at",
                    (item['item_id'], item['name'], item['updated_at']))
        conn.commit()

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    conn = get_connection()
    for message in consumer:
        item = message.value
        insert_item(conn, item)
        print(f"[Consumer] Inserted/Updated: {item}")

if __name__ == '__main__':
    main()
