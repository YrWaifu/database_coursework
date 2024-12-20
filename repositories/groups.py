import psycopg2

from settings import DB_CONFIG


def insert(name):
    query = """
        INSERT INTO groups (name)
        VALUES (%s)
        RETURNING id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [name])

def delete(employee_id):
    query = """
        DELETE FROM groups
        WHERE employee_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [employee_id])

def check_amount(name):
    query = """
        SELECT COUNT(*) FROM groups WHERE name = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [name])
            return cur.fetchone()

def get_by_name(name):
    query = """
        SELECT * 
        FROM groups 
        WHERE name = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [name])
            return cur.fetchone()