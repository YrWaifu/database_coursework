from datetime import datetime
import psycopg2
import streamlit as st
from st_aggrid import AgGrid

from repositories import employees, testdrives, helicopters
from database import enum

def add_testdrive():
    with st.expander("Добавление полета"):
        date = st.date_input("Дата полета")
        datetime_obj = datetime.combine(date, datetime.min.time())
        report = st.text_area("Текст отчета")
        employee_email = st.text_input("Email сотрудника")

        register_number = st.text_input("Регистрационный номер вертолета")

        if st.button("Отправить", key=1):
            if not employees.get_by_email(employee_email):
                st.error("Такой сотрудник не существует")
                return
            employee_id = employees.get_by_email(employee_email)[0]
            if not helicopters.get_by_register_number(register_number):
                st.error("Такой вертолет отсутствует в базе")
                return
            helicopter_id = helicopters.get_by_register_number(register_number)[0]
            # print("-------------\n", date, report, employee_id, helicopter_id, "\n---------\n")
            try:
                testdrives.insert(date, report, employee_id, helicopter_id)
            except psycopg2.errors.UniqueViolation:
                st.success("Такой полет уже добавлен")
                return

            st.success("Полет успешно добавлен!")

def watch_report():
    with st.expander("Посмотреть отчет"):
        testdrive_id = st.text_input("Id полета из таблицы ниже")

        if st.button("Отправить", key=12):
            try:
                st.markdown(testdrives.get_report(testdrive_id))
            except TypeError:
                st.error("Такого полета не существует")


def show_all():
    df = testdrives.show()
    AgGrid(df, fit_columns_on_grid_load=True)


if ("user_id" in st.session_state) and (employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo):
    add_testdrive()

if "user_id" in st.session_state:
    watch_report()
    show_all()