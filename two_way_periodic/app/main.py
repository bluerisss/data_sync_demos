import os
import time
import psycopg2
from datetime import datetime

DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_A_HOST = os.environ['DB_A_HOST']
DB_B_HOST = os.environ['DB_B_HOST']
DB_A_NAME = os.environ['DB_A_NAME']
DB_B_NAME = os.environ['DB_B_NAME']
SYNC_INTERVAL = int(os.environ.get('SYNC_INTERVAL', 30))

def get_connection(host, dbname):
    return psycopg2.connect(
        host=host,
        dbname=dbname,
        user=DB_USER,
        password=DB_PASS
    )

def fetch_items(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, updated_at FROM items")
        return cur.fetchall()

def upsert_item(conn, item):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO items (id, name, updated_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET name = EXCLUDED.name,
                updated_at = EXCLUDED.updated_at
            WHERE items.updated_at < EXCLUDED.updated_at
        """, (item[0], item[1], item[2]))
        conn.commit()

def sync(source_conn, target_conn):
    items = fetch_items(source_conn)
    for item in items:
        upsert_item(target_conn, item)

def main():
    conn_a = get_connection(DB_A_HOST, DB_A_NAME)
    conn_b = get_connection(DB_B_HOST, DB_B_NAME)

    while True:
        print(f"[{datetime.now()}] Syncing A -> B")
        sync(conn_a, conn_b)

        print(f"[{datetime.now()}] Syncing B -> A")
        sync(conn_b, conn_a)

        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    main()
