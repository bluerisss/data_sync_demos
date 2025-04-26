CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS item_changes (
  id SERIAL PRIMARY KEY,
  item_id INTEGER,
  name TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION log_item_change() RETURNS trigger AS $$
BEGIN
  INSERT INTO item_changes (item_id, name, updated_at)
  VALUES (NEW.id, NEW.name, NEW.updated_at);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER item_change_trigger
AFTER INSERT OR UPDATE ON items
FOR EACH ROW
EXECUTE FUNCTION log_item_change();

INSERT INTO items (name) VALUES ('Initial Item A');
