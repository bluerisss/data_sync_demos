1. Run Docker Compose
```bash
docker compose up --build
```

2. Access source_db to insert data

Open a new terminal and access source_db:
```bash
docker exec -it source_db psql -U user -d sourcedb
```

Insert data:
```sql
INSERT INTO items (id, name, updated_at) VALUES (1, 'Item A', NOW());
UPDATE items SET name = 'Item A Updated' WHERE id = 1;
```

3. Check target_db:
```bash
docker exec -it target_db psql -U user -d targetdb
SELECT * FROM items;
```
