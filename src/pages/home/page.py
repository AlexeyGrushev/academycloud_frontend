import streamlit
from streamlit_option_menu import option_menu
from streamlit_cookies_controller import CookieController

from src.pages.main.page import MainPage
from src.pages.profile.setup_profile_page import SetupProfile
from src.utils.get_profile import get_user_profile
from src.utils.logout import logout
from src.utils.config import settings


class RootPage:
    def __init__(self, st: streamlit, cookie_manager: CookieController):
        self.st = st
        self.cookie_manager = cookie_manager
        self.markdown()
        pass

    def sidebar_nav_menu(self):
        buttons = [
            "Главная",
            "Задания",
            "Быстрые задания",
            "Профиль"
        ]
        with self.st.sidebar:
            option = option_menu(
                menu_title="Меню",
                options=buttons
            )
        return option

    def markdown(self):
        profile = get_user_profile(self.cookie_manager.get("user_access"))

        if profile is None:
            try:
                logout(self.st, self.cookie_manager)
                self.st.toast(
                    ":yellow[При выполнении запроса произошла ошибка]",
                    icon="⚠️"
                )
            except Exception:
                pass

        if (
            profile["first_name"] is None or
            profile["last_name"] is None
        ):
            SetupProfile(self.st, self.cookie_manager)
            return

        side_col1, side_col2 = self.st.sidebar.columns(2)

        if profile["profile_pic"]:
            side_col1.image(
                f"{settings.API_URL}/image/{profile['profile_pic']}",
                width=96
            )
        else:
            side_col1.image(
                f"{settings.API_URL}/image/profile_pic_default.jpeg",
                width=96
            )

        side_col2.subheader(
            f"{profile['first_name']} {profile['last_name']}"
        )
        side_col2.text("Опыт")

        menu = self.sidebar_nav_menu()

        if menu == "Главная":
            MainPage()
        elif menu == "Задания":
            ...

        logout_btn = self.st.sidebar.button("Выйти")
        if logout_btn:
            logout(self.st, self.cookie_manager)
