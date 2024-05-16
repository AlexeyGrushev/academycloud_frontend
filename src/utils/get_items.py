import requests

from streamlit_cookies_controller import CookieController

from src.utils.config import settings


def get_items(cookie_manager: CookieController) -> dict | None:
    headers = {
        'accept': 'application/json',
    }

    cookies = cookie_manager.getAll()

    response = requests.get(
        f'{settings.API_URL}/api/v1/lesson/get_items',
        headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
