import requests

from streamlit_cookies_controller import CookieController

from src.utils.config import settings


def get_lesson(
        lesson_id: int, cookie_manager: CookieController) -> dict | None:
    headers = {
        'accept': 'application/json',
    }

    params = {
        'lesson_id': str(lesson_id),
    }

    cookies = {
        "user_access": cookie_manager.get("user_access")
    }

    response = requests.get(
        f'{settings.API_URL}/api/v1/lesson/get_lesson?lesson_id=5',
        params=params, headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
