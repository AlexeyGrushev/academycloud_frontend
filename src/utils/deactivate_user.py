import requests

from src.utils.config import settings


def deactivate_user(token: str):

    headers = {
        'accept': 'application/json',
    }

    cookies = {
        "user_access": token
    }

    response = requests.delete(
        f'{settings.API_URL}/api/v1/user/deactivate_user',
        headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
