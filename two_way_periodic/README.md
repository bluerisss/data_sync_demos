# Two Way Periodic Sync Demo

- Run Docker Compose

  ```bash
  docker compose up --build
  ```

- Access db_a to insert data

  Open a new terminal and access db_a:

  ```bash
  docker exec -it db_a psql -U postgres -d db_a
  ```

  Insert data:

  ```sql
  INSERT INTO items (id, name, updated_at) VALUES (1, 'Item A', NOW());
  ```

  Update data:

  ```sql
  UPDATE items SET name = 'Item A Updated from db_a', updated_at = NOW() WHERE id = 1;
  ```

- Access db_b to update data

  Open a new terminal and access db_b:

  ```bash
  docker exec -it db_b psql -U postgres -d db_b
  ```

  Update data:

  ```sql
  UPDATE items SET name = 'Item A Updated from db_b', updated_at = NOW() WHERE id = 1;
  ```

- Check db_b:

  ```bash
  docker exec -it db_b psql -U postgres -d db_b
  SELECT * FROM items;
  ```
