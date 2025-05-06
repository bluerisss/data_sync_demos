import os
import psycopg2
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    os.environ['TOPIC'],
    bootstrap_servers=os.environ['KAFKA_BOOTSTRAP_SERVERS'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )

def apply_change(event):
    conn = get_db_connection()
    cur = conn.cursor()
    op = event['operation']
    data = event['data']
    if op == 'INSERT':
        cur.execute("INSERT INTO items (id, name, updated_at) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING", (data['id'], data['name'], data['updated_at']))
    elif op == 'UPDATE':
        cur.execute("UPDATE items SET name=%s, updated_at=%s WHERE id=%s", (data['name'], data['updated_at'], data['id']))
    elif op == 'DELETE':
        cur.execute("DELETE FROM items WHERE id=%s", (data['id'],))
    conn.commit()
    cur.close()
    conn.close()

def consume():
    for msg in consumer:
        event = msg.value
        print(f"Received at B: {event}")
        apply_change(event)

if __name__ == '__main__':
    consume()
