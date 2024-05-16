import requests

from src.utils.config import settings


def send_confirm_email(token: str):

    headers = {
        'accept': 'application/json',
    }

    cookies = {
        "user_access": token
    }

    response = requests.get(
        f'{settings.API_URL}/api/v1/user/send_confirm_email',
        headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
