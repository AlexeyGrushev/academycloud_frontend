import streamlit
import time
from streamlit_cookies_controller import CookieController

from src.utils.login import login_user
from src.utils.register import register_user


class AuthPage:
    def __init__(self, st: streamlit, cookie_manager: CookieController):
        self.st = st
        self.cookie_manager = cookie_manager
        self.auth_markdown()
        pass

    def auth_markdown(self):
        col1, col2 = self.st.sidebar.columns(2)

        col1.image("src/static/img/logo.png")
        col2.subheader("Онлайн обучение учебным дисциплинам")

        auth, reg, restore = self.st.sidebar.tabs(
            [
                "Авторизация",
                "Регистрация",
                "Восстановление доступа"
            ]
        )

        login = auth.text_input("Логин или Email")
        password = auth.text_input("Пароль", type="password")
        auth_button = auth.button("Войти")

        if auth_button:
            login_user(
                self.st,
                self.cookie_manager,
                login,
                password
            )

        email = reg.text_input("Почта")
        login = reg.text_input("Логин")
        password = reg.text_input("Парoль", type="password")
        retry_password = reg.text_input(
            "Повторите пароль", type="password")
        register_button = reg.button("Зарегистрироваться")

        login_data = restore.text_input("Email или логин")
        restore_button = restore.button("Отправить письмо")

        if restore_button:
            print("Заглушка")

        if register_button:
            if register_user(
                self.st,
                email,
                login,
                password,
                retry_password
            ):
                time.sleep(1)
                login_user(
                    self.st,
                    self.cookie_manager,
                    login,
                    password
                )
