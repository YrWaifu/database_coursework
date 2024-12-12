import psycopg2

from settings import DB_CONFIG


def insert(name, employee_id):
    query = """
        INSERT INTO groups (name, employee_id)
        VALUES (%s, %s)
        RETURNING id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [name, employee_id])
            return cur.fetchone()[0]

def delete(employee_id):
    query = """
        DELETE FROM groups
        WHERE employee_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [employee_id])

def check_amount(employee_id):
    query = """
        SELECT COUNT(*) FROM groups WHERE employee_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [employee_id])
            return cur.fetchone()