CREATE OR REPLACE FUNCTION check_client_family_head_constraint()
RETURNS TRIGGER AS $$
BEGIN
    -- New client's head cannot already be in client column, as it means it has a head itself  
    IF EXISTS (SELECT 1 FROM client_family WHERE client = NEW.family_head) THEN
        RAISE EXCEPTION 'A client head cannot already exist as a client with its own head';
    END IF;
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_check_client_family_head_constraint
BEFORE INSERT OR UPDATE ON client_family
FOR EACH ROW 
EXECUTE FUNCTION check_client_family_head_constraint();