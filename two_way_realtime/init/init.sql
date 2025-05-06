CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE item_changes (
    id SERIAL PRIMARY KEY,
    item_id INT,
    operation TEXT,
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION notify_item_change() RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO item_changes (item_id, operation, data)
        VALUES (NEW.id, TG_OP, row_to_json(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO item_changes (item_id, operation, data)
        VALUES (NEW.id, TG_OP, row_to_json(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO item_changes (item_id, operation, data)
        VALUES (OLD.id, TG_OP, row_to_json(OLD));
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_items_changes
AFTER INSERT OR UPDATE OR DELETE ON items
FOR EACH ROW EXECUTE FUNCTION notify_item_change();
