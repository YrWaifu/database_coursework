import psycopg2
import pandas as pd
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
        SELECT id, name, password_hash, email, title
        FROM employees
        WHERE id = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [id])
            return cur.fetchone()

def show():
    query = """
        SELECT e.name, e.email, e.title, gg.name as group_name
        FROM employees e
        LEFT JOIN group_employee ge ON e.id = ge.employee_id
        LEFT JOIN groups gg ON ge.group_id = gg.id 
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])

            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            return df