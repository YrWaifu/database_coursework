import psycopg2
import streamlit as st
from repositories import parts, employees
from database import enum

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



if ("user_id" in st.session_state) and ((employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo) or (employees.get_by_id(st.session_state["user_id"])[4] == enum.engineer)):
    add_part()
    delete_part()