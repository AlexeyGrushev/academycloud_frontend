import streamlit
import requests

from streamlit_cookies_controller import CookieController

from pages.profile.schemas import SUpdateUser
from src.utils.config import settings
from utils.authentificate_user import authentificate_user


def update_user(
        st: streamlit, cookie_manager: CookieController,
        login_data: str, password: str,
        data: SUpdateUser):
    auth_response = authentificate_user(login_data, password)

    if auth_response.status_code == 200:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            'email': data.email,
            'login': data.login,
            'password': data.password,
        }

        cookies = {
            "user_access": cookie_manager.get("user_access")
        }

        response = requests.put(
            f'{settings.API_URL}/api/v1/user/update_user',
            headers=headers, json=json_data, cookies=cookies)

        if response.status_code == 200:
            response = response.json()

            if response["updated_email"] is True:
                st.toast(
                    ":green[Email успешно обновлен]",
                    icon="✅"
                )
            elif response["updated_email"] == "Failed. Email exists":
                st.toast(
                    ":red[Не удалось обновить Email."
                    " Этот Email уже используется]",
                    icon="❌"
                )
            if response["updated_login"]:
                st.toast(
                    ":green[Логин успешно обновлен]",
                    icon="✅"
                )
            if response["updated_password"]:
                st.toast(
                    ":green[Пароль успешно обновлен]",
                    icon="✅"
                )
            return
        else:
            st.toast(
                ":yellow[Не удалось обновить информацию о пользователе]",
                icon="⚠️"
            )
    else:
        st.toast(
            ":red[Вы ввели неверный пароль]",
            icon="❌"
        )
