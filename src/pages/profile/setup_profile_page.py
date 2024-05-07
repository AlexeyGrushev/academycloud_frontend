import streamlit as st

from PIL import Image
from streamlit_cookies_controller import CookieController

from src.utils.logout import logout
from src.utils.config import settings
from src.utils.update_profile import update_user_profile


class SetupProfile:
    def __init__(self, st, cookie_manager: CookieController) -> None:
        self.st = st
        self.cookie_manager = cookie_manager
        self.markdown()
        pass

    def markdown(self):
        st.title("Добро пожаловать в Academy Cloud!")
        st.subheader(
            "Необходимо заполнить Ваш профиль перед тем как продолжить")

        col1, col2 = self.st.columns(2)

        image = None

        try:
            image_view = col1.empty()

            image_view.image(
                f"{settings.API_URL}/image/profile_pic_default.jpeg",
                width=150
            )
        except Exception:
            col1.text("Кажется что-то пошло не так🤔")

        profile_pic = col2.file_uploader(
            "Загрузите изображение профиля", type=["png", "jpg", "jpeg"],
        )
        col2.text("Самый идеальный размер изображения составляет 150x150 px.")

        first_name = self.st.text_input("Имя *")
        last_name = self.st.text_input("Фамилия *")
        status = self.st.text_area("Статус профиля", max_chars=200)

        self.st.text("* Обязательно для заполнения")

        submit_btn = self.st.button("Сохранить")

        if profile_pic:
            image = Image.open(profile_pic).resize(
                (150, 150)
            )
            image_view.image(
                image,
                width=150
            )

        if submit_btn:
            update_user_profile(
                self.st,
                self.cookie_manager,
                first_name.replace(" ", ""),
                last_name.replace(" ", ""),
                status,
                profile_pic
            )

        logout_btn = self.st.button("Выйти")
        if logout_btn:
            logout(self.st, self.cookie_manager)
