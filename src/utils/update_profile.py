import time
import requests
import streamlit

from streamlit_cookies_controller import CookieController

from src.utils.config import settings
from src.utils.get_profile import get_user_profile
from src.utils.upload_file import upload_file
from utils.right_rerun import right_rerun


def profile_request(
    token,
    first_name,
    last_name,
    status
) -> requests.Response:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'first_name': first_name,
        'last_name': last_name,
        'status': status,
    }

    cookies = {
        "user_access": token
    }

    response = requests.put(
        f'{settings.API_URL}/api/v1/user/update_profile',
        headers=headers,
        json=json_data,
        cookies=cookies
    )

    return response


def update_user_profile(
    st: streamlit,
    cookie_manager: CookieController,
    first_name: str,
    last_name: str,
    status: str,
    image_file
):
    token = cookie_manager.get("user_access")
    profile = get_user_profile(
        token
    )

    if first_name == "":
        st.toast(
            ":red[Имя не может быть пустым]",
            icon="❌"
        )
        return

    if last_name == "":
        st.toast(
            ":red[Фамилия не может быть пустой]",
            icon="❌"
        )
        return

    if (
        profile["first_name"] != first_name or
        profile["last_name"] != last_name or
        profile["status"] != status
    ):
        profile_res = profile_request(
            token,
            first_name,
            last_name,
            status
        )

        if profile_res.status_code == 200:
            st.toast(
                ":green[Информация о профиле обновлена]",
                icon="✅"
            )

    if image_file is not None:
        image_res = upload_file(
            1,
            token,
            image_file
        )

        if image_res.status_code == 200:
            st.toast(
                ":green[Картинка профиля обновлена]",
                icon="✅"
            )

    time.sleep(1)
    right_rerun(st, cookie_manager)
