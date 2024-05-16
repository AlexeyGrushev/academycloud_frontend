import requests

from datetime import date

from src.utils.config import settings


def get_scoreboard(
    token: str,
    start_date: date,
    end_date: date
):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'start_date': start_date,
        'end_date': end_date,
    }

    cookies = {
        "user_access": token
    }

    response = requests.post(
        f'{settings.API_URL}/api/v1/user/get_user_rating',
        headers=headers, json=json_data, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
