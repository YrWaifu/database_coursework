import psycopg2


def up(db_config):
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE audit_log (
                    id SERIAL PRIMARY KEY,       
                    employee_id INT NOT NULL,       
                    action VARCHAR(50) NOT NULL,   
                    changed_at TIMESTAMP NOT NULL,  
                    details TEXT                    
                );
                    
                CREATE OR REPLACE FUNCTION log_employee_update()
                RETURNS TRIGGER AS $$
                BEGIN
                    INSERT INTO audit_log (employee_id, action, changed_at)
                    VALUES (NEW.id, 'UPDATE', NOW());
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                
                CREATE TRIGGER employee_update_trigger
                AFTER INSERT ON employees
                FOR EACH ROW
                EXECUTE FUNCTION log_employee_update();
            """)
