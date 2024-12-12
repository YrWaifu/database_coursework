import psycopg2
import streamlit as st
from repositories import helicopters, employees, parts, helicopter_parts
from database import enum

def add_helicopter():
    with st.expander("Добавление нового вертолета"):
        model = st.text_input("Модель")
        name = st.text_input("Название")
        register_number = st.text_input("Регистрационный номер", key=1)

        if st.button("Отправить", key=2):
            try:
                helicopters.insert(model, name, register_number)
            except psycopg2.errors.UniqueViolation:
                st.success("Вертолет с таким серийным номером уже добавлен")
                return

            st.success("Вертолет успешно добавлен!")
            st.write("Вы ввели:")
            st.write(f"Модель: {model}")
            st.write(f"Название: {name}")
            st.write(f"Регистрационный номер: {register_number}")

def delete_helicopter():
    with st.expander("Удаление вертолета"):
        register_number = st.text_input("Регистрационный номер", key=3)

        if st.button("Отправить", key=4):
            try:
                helicopters.delete(register_number)
            except psycopg2.errors.UniqueViolation:
                st.success("Вертолет с таким регистрационным номером уже добавлен")
                return

            st.success(f"Вертолет с регистрационным номером {register_number} успешно удален!")

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

def delete_part():
    with st.expander("Отвязать деталь"):
        serial_number = st.text_input("Серийный номер", key=10)
        part_id = parts.get_by_serial_number(serial_number)
        if not part_id:
            st.error("Деталь с таким серийным номером или отсутствует, или никуда не привязана")
            return
        part_id = part_id[0]
        helicopter_id = helicopter_parts.get_by_part_id(part_id)[0]
        helicopter = helicopters.get_by_id(helicopter_id)

        if st.button("Отправить", key=43):
            helicopter_parts.delete(part_id)

            st.success(f"Деталь с регистрационным номером {serial_number} успешно отвязана от вертолета {helicopter[1]} с серийным номером {helicopter[-1]}!")



if ("user_id" in st.session_state) and (employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo):
    add_helicopter()
    delete_helicopter()
    if (employees.get_by_id(st.session_state["user_id"])[4] == enum.engineer) or (employees.get_by_id(st.session_state["user_id"])[4] == enum.сeo):
        connection_helicopter_part()
        delete_part()