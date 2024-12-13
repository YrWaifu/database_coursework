import psycopg2

from settings import DB_CONFIG


def insert(group_id, employee_id):
    query = """
        INSERT INTO group_employee (group_id, employee_id)
        VALUES (%s, %s);
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [group_id, employee_id])

def delete(employee_id):
    query = """
        DELETE FROM group_employee
        WHERE employee_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [employee_id])

def check_amount(employee_id):
    query = """
        SELECT COUNT(*) FROM group_employee WHERE employee_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [employee_id])
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