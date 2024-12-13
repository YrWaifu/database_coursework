import psycopg2
import streamlit as st
from st_aggrid import AgGrid

from repositories import parts, employees, helicopters, helicopter_parts
from database import enum
from repositories.helicopter_parts import get_parts_helicopter
from services.auth import register


def add_part():
    with st.expander("Добавление новой детали вертолета"):
        name = st.text_input("Название")
        drawing_number = st.text_input("Чертежный номер (если есть)")
        serial_number = st.text_input("Серийный номер", key=1)

        if st.button("Отправить", key=2):
            try:
                parts.insert(name, drawing_number, serial_number)
            except psycopg2.errors.UniqueViolation:
                st.success("Деталь с таким серийным номером уже добавлена")
                return

            st.success("Деталь успешно добавлен!")
            st.write("Вы ввели:")
            st.write(f"Название: {name}")
            st.write(f"Чертежный номер: {drawing_number}")
            st.write(f"Серийный номер: {serial_number}")

def delete_part():
    with st.expander("Удаление детали"):
        serial_number = st.text_input("Серийный номер", key=3)

        if st.button("Отправить", key=4):
            try:
                parts.delete(serial_number)
            except psycopg2.errors.UniqueViolation:
                st.success("Деталь с таким серийным номером уже добавлен")
                return

            st.success(f"Деталь с регистрационным номером {serial_number} успешно удален!")


def show_helicopter_parts():
    with st.expander("Посмотреть детали вертолета"):
        register_number = st.text_input("Регистрационный номер", key=231)
        helicopter = helicopters.get_by_register_number(register_number)

        if st.button("Отправить", key=23123):
            if not helicopter:
                st.error("Такого вертолета не существует")
            df = helicopter_parts.get_parts_helicopter(helicopter[0])
            AgGrid(df, fit_columns_on_grid_load=True)

def connection_helicopter_part():
    with st.expander("Привязать деталь к вертолету"):
        register_number = st.text_input("Регистрационный номер вертолета", key=5)
        serial_number = st.text_input("Серийный номер детали", key=7)

        if st.button("Отправить", key=6):
            helicopter = helicopters.get_by_register_number(register_number)
            part = parts.get_by_serial_number(serial_number)

            if not helicopter:
                st.error("Вертолет с таким регистрационным номером отсутствует")
                return
            if not part:
                st.error("Деталь с таким серийным номером отсутствует")
                return
            if helicopter_parts.check_amount(part[0])[0] > 0:
                st.error("Деталь уже используется")
                return

            helicopter_parts.insert(helicopter[0], part[0])
            st.success(f"Деталь успешно привязана")


if ("user_id" in st.session_state) and ((employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo) or (employees.get_by_id(st.session_state["user_id"])[4] == enum.engineer)):
    add_part()
    delete_part()
    connection_helicopter_part()
    show_helicopter_parts()