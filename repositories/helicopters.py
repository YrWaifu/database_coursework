import psycopg2

from settings import DB_CONFIG


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