import streamlit as st
from streamlit.components.v1 import html

# Определите ваш JavaScript код
my_js = """
function myFunction() {
    // Ваш код здесь
    alert("Hola mundo");

    if (someCondition) {
        return;  // Завершает выполнение функции, если someCondition истинно
    }

    // Дополнительный код здесь
}

"""

# Оберните JavaScript код в HTML
my_html = f"<script>{my_js}</script>"

# Выполните ваше приложение
st.title("Пример JavaScript")
if st.button("Test"):
    html(my_html)
