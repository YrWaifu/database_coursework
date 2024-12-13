from tokenize import group

import psycopg2
import streamlit as st
from st_aggrid import AgGrid

from repositories import employees, groups, group_employee
from database import enum

def add_group():
    with st.expander("Добавление сотрудника в группу"):
        name = st.text_input("Название группы")
        employee_email = st.text_input("Email сотрудника")

        if st.button("Отправить", key=2):
            if not employees.get_by_email(employee_email):
                st.error("Такой сотрудник не существует")
                return
            employee_id = employees.get_by_email(employee_email)[0]

            if groups.check_amount(name)[0] == 0:
                groups.insert(name)
            group_id = groups.get_by_name(name)[0]

            print(groups.check_amount(name), group_id, employee_id)

            if group_employee.check_amount(employee_id):
                group_employee.delete(employee_id)

            group_employee.insert(group_id, employee_id)

            st.success(f"Сотрудник с почтой {employee_email} успешно добавлен в группу {name}!")

def show_all():
    df = employees.show()
    AgGrid(df, fit_columns_on_grid_load=True)


if ("user_id" in st.session_state) and (employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo):
    add_group()

if "user_id" in st.session_state:
    show_all()
