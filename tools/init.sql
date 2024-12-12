-- Создание ENUM для должностей, если он ещё не существует
DO $$ BEGIN
    CREATE TYPE job_title AS ENUM ('генеральный директор', 'программист', 'инженер', 'пилот');
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
    name VARCHAR(100) NOT NULL
);

-- Создание таблицы Helicopter
CREATE TABLE helicopters (
    id SERIAL PRIMARY KEY,
    model VARCHAR(100) NOT NULL
);

-- Создание таблицы Parts
CREATE TABLE parts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Создание таблицы TestDrive
CREATE TABLE testdrives (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    report TEXT,
    employee_id INT REFERENCES employees (id),
    helicopter_id INT REFERENCES helicopter (id)
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
);
