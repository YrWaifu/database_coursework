import streamlit as st


from services import auth

st.title("Аутентификация")
username = st.text_input("Введите почту")
password = st.text_input("Введите пароль", type="password")
if st.button("Войти"):
    user_id = auth.auth(username, password)
    if user_id:
        st.session_state["user_id"] = user_id
        st.success("Аутентификация прошла успешно!")
    else:
        st.success("Неверная почта или пароль")