import streamlit
import time
from streamlit_cookies_controller import CookieController

from src.utils.login import login_user
from src.utils.register import register_user
from utils.restore_account import restore_account


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

        if auth_button or password:
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
            restore_account(login_data)
            self.st.toast(
                ":blue[Если введены верные данные,"
                " то Вы получите письмо на почту]",
                icon="ℹ"
            )

        self.st.title(
            ":blue[Academy Cloud]. Облако знаний в шаге от Вас!"
        )
        self.st.subheader("")
        self.st.subheader("")

        col1, col2 = self.st.columns(2)

        col1.image(
            "src/static/img/eductation_gif.gif",
            width=380)
        col2.markdown(
            "**Гибкость и доступность:** Обучение доступно в любое время и"
            " в любом месте, где есть интернет."
        )
        col2.markdown(
            "**Персонализация:** Каждый пользователь может выбрать курсы,"
            " которые соответствуют его интересам и потребностям."
        )
        col2.markdown(
            "**Широкий спектр курсов:** Academy Cloud предлагает курсы по"
            " различным темам, от технических до гуманитарных."
        )
        col2.markdown(
            "**Обновляемость материалов:** Все курсы регулярно обновляются,"
            " чтобы оставаться актуальными и соответствовать последним"
            " трендам и технологиям."
        )
        col2.markdown("**Academy Cloud - ваш ключ к образованию будущего!**")

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
