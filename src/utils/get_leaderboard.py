from datetime import date
import requests

from src.utils.config import settings


def get_leaderboard(
    token: str,
    limit: int,
    start_date: date | str | None,
    end_date: date | str | None
):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    params = {
        'limit': str(limit),
    }

    json_data = {
        'start_date': start_date,
        'end_date': end_date,
    }

    cookies = {
        "user_access": token
    }

    response = requests.post(
        f'{settings.API_URL}/api/v1/user/get_users_leaderboard',
        params=params, headers=headers, json=json_data, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return None
