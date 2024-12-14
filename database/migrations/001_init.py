import psycopg2


def up(db_config):
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            select count(*) from information_schema.tables where table_schema = 'public'
            """)
            if cur.fetchone()[0] > 0:
                return
        with conn.cursor() as cur:
            cur.execute("""
                -- Создание ENUM для должностей, если он ещё не существует
                DO $$ BEGIN
                    CREATE TYPE job_title AS ENUM ('генеральный директор', 'инженер', 'пилот');
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            
                -- Создание таблицы Employee
                CREATE TABLE employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    title job_title NOT NULL
                );
            
                -- Создание таблицы Group
                CREATE TABLE groups (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    employee_id INT REFERENCES employees (id)
                );
            
                -- Создание таблицы Helicopter
                CREATE TABLE helicopters (
                    id SERIAL PRIMARY KEY,
                    model VARCHAR(100) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    register_number VARCHAR(100) UNIQUE NOT NULL
                );
            
                -- Создание таблицы Parts
                CREATE TABLE parts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    drawing_number VARCHAR(100),
                    serial_number VARCHAR(100) UNIQUE NOT NULL
                );
            
                -- Создание таблицы TestDrive
                CREATE TABLE testdrives (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL,
                    report TEXT,
                    employee_id INT REFERENCES employees (id),
                    helicopter_id INT REFERENCES helicopters (id)
                );
            
                -- Создание таблицы GroupHelicopter
                CREATE TABLE group_helicopter (
                    group_id INT REFERENCES groups (id),
                    helicopter_id INT REFERENCES helicopters (id),
                    PRIMARY KEY (group_id, helicopter_id)
                );
            
                -- Создание таблицы HelicopterParts
                CREATE TABLE helicopter_parts (
                    helicopter_id INT REFERENCES helicopters (id),
                    part_id INT REFERENCES parts (id),
                    PRIMARY KEY (helicopter_id, part_id)
                );"""
                )


def down(db_config):
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE helicopter_parts;
                DROP TABLE group_helicopter;
                DROP TABLE testdrives;
                DROP TABLE parts;
                DROP TABLE helicopters;
                DROP TABLE groups;
                DROP TABLE employees;
            """)
