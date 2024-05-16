import requests

from src.utils.config import settings


def authentificate_user(login_data: str, password: str) -> requests.Response:
    payload = {
        "login_data": login_data,
        "password": password
    }

    request = requests.post(
        url=f"{settings.API_URL}/api/v1/auth/login",
        json=payload
    )

    return request
