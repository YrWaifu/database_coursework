import psycopg2

from settings import DB_CONFIG


def insert(name, drawing_number, serial_number):
    query = """
        INSERT INTO parts (name, drawing_number, serial_number)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [name, drawing_number, serial_number])
            return cur.fetchone()[0]

def delete(serial_number):
    query = """
        DELETE FROM parts
        WHERE serial_number = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [serial_number])

def get_by_serial_number(serial_number):
    query = """
        SELECT *
        FROM parts
        WHERE serial_number = %s
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [serial_number])
            return cur.fetchone()