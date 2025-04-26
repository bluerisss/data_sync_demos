#!/usr/bin/env python3

import psycopg2
import os

source_conn = psycopg2.connect(
    host='source_db', port=5432,
    dbname='sourcedb', user='user', password='pass'
)
target_conn = psycopg2.connect(
    host='target_db', port=5432,
    dbname='targetdb', user='user', password='pass'
)

source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()

source_cursor.execute("SELECT id, name, updated_at FROM items")
rows = source_cursor.fetchall()

for row in rows:
    target_cursor.execute(
        """
        INSERT INTO items (id, name, updated_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            updated_at = EXCLUDED.updated_at
        """,
        row
    )
target_conn.commit()

source_cursor.close()
target_cursor.close()
source_conn.close()
target_conn.close()
print("[SYNC] Data synced successfully.")
