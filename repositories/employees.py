import psycopg2

from settings import DB_CONFIG


def insert(name, email, password_hash, title):
    query = """
        INSERT INTO employees (name, email, password_hash, title)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [name, email, password_hash, title])
            return cur.fetchone()[0]

def get_by_email(email):
    query = """
        SELECT id, name, password_hash, email 
        FROM employees
        WHERE email = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [email])
            return cur.fetchone()

def get_by_id(id):
    query = """
        SELECT id, name, password_hash, email 
        FROM employees
        WHERE id = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [id])
            return cur.fetchone()