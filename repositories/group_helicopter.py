import psycopg2

from settings import DB_CONFIG


def insert(helicopter_id, group_id):
    query = """
        INSERT INTO group_helicopter (helicopter_id, group_id)
        VALUES (%s, %s);
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [helicopter_id, group_id])

def delete(helicopter, group):
    query = """
        DELETE FROM group_helicopter
        WHERE group_id = %s AND helicopter_id = %s;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, [group, helicopter])