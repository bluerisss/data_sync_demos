1. Run Docker Compose
```bash
docker compose up --build
```

2. Access db_a to insert data

Open a new terminal and access db_a:
```bash
docker exec -it db_a psql -U postgres -d db_a
```

Insert data:
```sql
INSERT INTO items (id, name, updated_at) VALUES (1, 'Item A', NOW());
```

Update data:
On db_a
```sql
UPDATE items SET name = 'Item A Updated from db_a', updated_at = NOW() WHERE id = 1;
```
On db_b
```sql
UPDATE items SET name = 'Item A Updated from db_b', updated_at = NOW() WHERE id = 1;
```

3. Check db_b:
```bash
docker exec -it db_b psql -U postgres -d db_b
SELECT * FROM items;
```
