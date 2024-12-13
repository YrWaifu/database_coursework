import psycopg2


def up(db_config):
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                BEGIN;
            
                -- Создание таблицы GroupEmployees
                CREATE TABLE group_employee (
                    group_id INT REFERENCES groups (id),
                    employee_id INT REFERENCES employees (id),
                    PRIMARY KEY (group_id, employee_id)
                );
                
                insert INTO group_employee (group_id, employee_id)
                select first_value(id) over (partition by "name" order by id) as id, employee_id 
                from "groups"
                group by name, employee_id, groups.id;
                
                insert into group_helicopter (helicopter_id, group_id)
                with g as (
                    select distinct first_value(id) over (partition by "name" order by id) as id, name
                    from "groups"
                    group by name, groups.id
                )
                select gh.helicopter_id, (select g.id from g where g.name = sg.name)
                from group_helicopter gh
                left join "groups" sg on sg.id = gh.group_id
                on conflict do nothing;
                
                delete from group_helicopter where group_id not in (
                select distinct first_value(id) over (partition by "name" order by id) as id
                from "groups"
                group by name, groups.id
                );
                
                delete from groups where id not in (
                    select distinct first_value(id) over (partition by "name" order by id) as id
                    from "groups"
                    group by name, groups.id
                );
                
                ALTER TABLE groups DROP COLUMN employee_id CASCADE;
                
                COMMIT;
            """)
