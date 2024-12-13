import psycopg2


def up(db_config):
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                ALTER TABLE groups ADD CONSTRAINT groups_name_idx UNIQUE (name)
            """)
