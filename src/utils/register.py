import streamlit
import secrets
import requests

from pydantic import ValidationError

from src.pages.auth.schemas import SEmail, SPassword
from utils.config import settings


def register_user(
    st: streamlit,
    email: str,
    login: str,
    password: str,
    retry_password: str
) -> dict | None:
    error_status = False

    if (
        email == "" or
        login == "" or
        password == "" or
        retry_password == ""
    ):
        st.toast(
            ":red[Необходимо заполнить все поля]",
            icon="❌"
        )
        return

    if (
        " " in email or
        " " in login or
        " " in password or
        " " in retry_password
    ):
        st.toast(
            ":red[Регистрационные данные не должны содержать пробел]",
            icon="❌"
        )
        return

    if not secrets.compare_digest(
        password,
        retry_password
    ):
        st.toast(
            ":red[Пароли не совпадают]",
            icon="❌"
        )
        error_status = True

    try:
        SEmail(email=email)
    except ValidationError:
        st.toast(
            ":red[Введён неверный формат Email]",
            icon="❌"
        )
        error_status = True

    try:
        SPassword(password=password)
    except ValidationError:
        st.toast(
            ":red[Минимальная длина пароля состовляет 8 символов]",
            icon="❌"
        )
        error_status = True

    if error_status:
        return
    else:
        payload = {
            "email": email,
            "login": login,
            "password": password
        }
        try:
            request = requests.post(
                url=f"{settings.API_URL}/api/v1/auth/register",
                json=payload
            )

            if request.status_code == 200:
                st.toast(
                    ":green[Пользователь успешно зарегистрирован]",
                    icon="✅"
                )
                return True

            elif request.status_code == 400:
                st.toast(
                    ":red[Такой пользователь уже зарегистрирован]",
                    icon="❌"
                )

        except Exception:
            st.toast(
                ":yellow[При выполнении запроса произошла ошибка]",
                icon="⚠️"
            )
            return
