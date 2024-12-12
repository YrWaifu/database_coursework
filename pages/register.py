import psycopg2
import streamlit as st
from database import enum
from services import auth


def register():
    try:
        auth.register(name, email, password, job_title)
    except psycopg2.errors.UniqueViolation:
        st.success("Пользователь с такой почтой уже существует")
    st.success("Регистрация прошла успешно!")


st.title("Регистрация")
email = st.text_input("Введите почту")
name = st.text_input("Введите ФИО")
password = st.text_input("Введите пароль", type="password")
job_title = st.selectbox(
    "Выберите долнжость:",
    (enum.engineer, enum.pilot)
)

st.button("Зарегистрироваться", on_click=register)
