1. Run Docker Compose
```bash
docker compose up --build
```

- This starts two PostgreSQL containers (source and target)
- It also runs sync_app with a cron job that synchronizes data from source_db to target_db every minute

2. Access source_db to insert data

Open a new terminal and access source_db:
```bash
docker exec -it source_db psql -U user -d sourcedb
```

Insert data:
```sql
INSERT INTO items (name) VALUES ('New item from source');
```

3. Wait for 1 minute (cron runs) and check target_db:
```bash
docker exec -it target_db psql -U user -d targetdb
SELECT * FROM items;
```

4. Monitor logs to ensure the cron job is running:
```bash
docker logs sync_app
```
