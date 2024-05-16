import requests

from streamlit_cookies_controller import CookieController

from src.utils.config import settings


def confirm_answers(
        lesson_id: int,
        data_to_send: list,
        cookie_manager: CookieController) -> dict | None:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'id': lesson_id,
        'answer': data_to_send
    }

    cookies = {
        "user_access": cookie_manager.get("user_access")
    }

    response = requests.post(
        f'{settings.API_URL}/api/v1/lesson/accept_lesson_answer',
        headers=headers, json=json_data, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
