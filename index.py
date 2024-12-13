import streamlit as st
from streamlit.runtime.media_file_storage import MediaFileStorageError

image_path = "images/main.jpeg"
try:
    st.image(image_path, use_container_width=True)
except MediaFileStorageError:
    st.text("Добро пожаловать в веб-сервис для автоматизации работы вертолетного завода.")