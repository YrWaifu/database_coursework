import streamlit as st
from repositories import employees

if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]

    user = employees.get_by_id(user_id)

    st.success(f"Привет, {user[1]}!!!!!")