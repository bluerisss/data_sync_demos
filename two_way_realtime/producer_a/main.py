import os
import time
import psycopg2
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=os.environ['KAFKA_BOOTSTRAP_SERVERS'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )

def poll_changes():
    conn = get_db_connection()
    cur = conn.cursor()
    last_id = 0
    while True:
        cur.execute("SELECT id, item_id, operation, data FROM item_changes WHERE id > %s ORDER BY id ASC", (last_id,))
        rows = cur.fetchall()
        for row in rows:
            last_id = row[0]
            event = {
                'item_id': row[1],
                'operation': row[2],
                'data': row[3]
            }
            producer.send(os.environ['TOPIC'], event)
            print(f"Sent from A: {event}")
        time.sleep(1)

if __name__ == '__main__':
    poll_changes()
