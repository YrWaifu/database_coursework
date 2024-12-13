import psycopg2

from settings import DB_CONFIG
import pandas as pd


def insert(model, name, register_number):
    query = """
        INSERT INTO helicopters (model, name, register_number)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [model, name, register_number])
            return cur.fetchone()[0]

def delete(register_number):
    query = """
        DELETE FROM helicopters
        WHERE register_number = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [register_number])

def get_by_register_number(register_number):
    query = """
        SELECT *
        FROM helicopters
        WHERE register_number = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [register_number])
            return cur.fetchone()

def get_by_id(id):
    query = """
        SELECT *
        FROM helicopters
        WHERE id = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [id])
            return cur.fetchone()

def show():
    query = """
        SELECT g.name as group_name, h.model, h.name, h.register_number
        FROM helicopters h
        LEFT JOIN group_helicopter gh ON h.id = gh.helicopter_id
        LEFT JOIN groups g ON gh.group_id = g.id
        GROUP BY g.name, h.model, h.name, h.register_number
        ORDER BY g.name
        ;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])

            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            return df