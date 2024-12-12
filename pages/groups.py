import psycopg2
import streamlit as st
from repositories import employees, groups
from database import enum

def add_group():
    with st.expander("Добавление новой группы"):
        name = st.text_input("Название группы")
        employee_email = st.text_input("Email сотрудника")

        if st.button("Отправить", key=2):
            if not employee_email:
                st.error("Такой сотрудник не существует")
                return
            employee_id = employees.get_by_email(employee_email)[0]

            if groups.check_amount(employee_id):
                groups.delete(employee_id)

            groups.insert(name, employee_id)

            st.success(f"Сотрудник с почтой {employee_email} успешно добавлен в группу {name}!")

if ("user_id" in st.session_state) and (employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo):
    add_group()