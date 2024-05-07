import requests
import logging

from utils.config import settings


def get_user_profile(token: str):
    try:
        cookies = {
            "user_access": token
        }
        request = requests.get(
            url=f"{settings.API_URL}/api/v1/user/get_user_info",
            cookies=cookies
        )

        if request.status_code == 200:
            return request.json()
        else:
            return None

    except Exception as ex_:
        logging.error(ex_)
        return None
