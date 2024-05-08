import requests

from src.utils.config import settings


def restore_account(login_data: str):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'login_data': login_data,
    }

    requests.post(
        f'{settings.API_URL}/api/v1/user/send_restore_email',
        headers=headers,
        json=json_data)
