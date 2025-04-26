# One Way Realtime Sync Demo

- Run Docker Compose

  ```bash
  docker compose up --build
  ```

- Access source_db to insert data

  Open a new terminal and access source_db:

  ```bash
  docker exec -it source_db_rt psql -U user -d sourcedb
  ```

  Insert data:

  ```sql
  INSERT INTO items (id, name, updated_at) VALUES (1, 'Item A', NOW());
  UPDATE items SET name = 'Item A Updated' WHERE id = 1;
  ```

- Check target_db:

  ```bash
  docker exec -it target_db_rt psql -U user -d targetdb
  SELECT * FROM items;
  ```
