import streamlit as st
from PIL import Image
import os

uploaded_file = st.file_uploader(
    "Загрузите изображение", type=["png", "jpg", "jpeg"],
    )

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image.save(os.path.join(
        '.', 'your_image_name.png'))
    st.image(image, caption='Загруженное изображение.', use_column_width=True)
