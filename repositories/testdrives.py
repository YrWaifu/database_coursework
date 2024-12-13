import psycopg2
import pandas as pd
from settings import DB_CONFIG


def insert(date, report, employee, helicopter):
    query = """
        INSERT INTO testdrives (date, report, employee_id, helicopter_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [date, report, employee, helicopter])
            return cur.fetchone()[0]

def show():
    query = """
        SELECT td.id, td.date, e.name as employeee, e.email, h.model, h.name as helicopter 
        FROM testdrives td
        LEFT JOIN employees e ON e.id = td.employee_id
        LEFT JOIN helicopters h ON h.id = td.helicopter_id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])

            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            return df

def amount(testdrive_id):
    query = """
        SELECT COUNT(*) FROM testdrives WHERE id = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [testdrive_id])

            return cur.fetchone()

def get_report(testdrive_id):
    query = """
        SELECT report FROM testdrives WHERE id = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [testdrive_id])

            return cur.fetchone()[0]