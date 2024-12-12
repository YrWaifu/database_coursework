import psycopg2

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