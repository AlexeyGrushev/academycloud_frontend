import requests

from streamlit_cookies_controller import CookieController

from src.utils.config import settings


def get_lessons(item_id: int, cookie_manager: CookieController) -> dict | None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'id': item_id,
    }

    cookies = {
        "user_access": cookie_manager.get("user_access")
    }

    response = requests.post(
        f'{settings.API_URL}/api/v1/lesson/get_lessons_by_item',
        headers=headers, json=json_data, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
