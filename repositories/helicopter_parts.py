import psycopg2
import pandas as pd
from settings import DB_CONFIG

def insert(helicopter_id, part_id):
    query = """
        INSERT INTO helicopter_parts (helicopter_id, part_id)
        VALUES (%s, %s);
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [helicopter_id, part_id])

def delete(part_id):
    query = """
        DELETE FROM helicopter_parts
        WHERE part_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [part_id])

def check_amount(part_id):
    query = """
        SELECT COUNT(*) FROM helicopter_parts WHERE part_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [part_id])
            return cur.fetchone()

def get_by_part_id(part_id):
    query = """
        SELECT * 
        FROM helicopter_parts 
        WHERE part_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [part_id])
            return cur.fetchone()

def get_parts_helicopter(helicopter_id):
    query = """
        SELECT h.name AS helicopter_name, h.model AS helicopter_model, p.name, p.drawing_number, p.serial_number
        FROM helicopter_parts hp
        LEFT JOIN parts p ON hp.part_id = p.id
        LEFT JOIN helicopters h ON hp.helicopter_id = h.id
        WHERE hp.helicopter_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [helicopter_id])

            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            return df