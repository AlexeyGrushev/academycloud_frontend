import streamlit as st


class MainPage:
    def __init__(self) -> None:
        self.st = st
        self.markdown()
        pass

    def markdown(self):
        self.st.header("Главная страница")
        self.st.subheader("[Ссылка на Гугл](https://www.google.ru/)")
