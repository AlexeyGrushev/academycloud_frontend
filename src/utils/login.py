import streamlit

from pydantic import ValidationError
from streamlit_cookies_controller import CookieController

from src.pages.auth.schemas import SPassword
from src.utils.right_rerun import right_rerun
from src.utils.authentificate_user import authentificate_user


def login_user(
    st: streamlit,
    cookie_manager: CookieController,
    login_data: str,
    password: str
):

    if (
        login_data == "" or
        password == ""
    ):
        st.toast(
            ":red[Необходимо заполнить все поля]",
            icon="❌"
        )
        return

    if " " in login_data:
        st.toast(
            ":red[Такого пользователя не существует]",
            icon="❌"
        )
        return

    try:
        SPassword(password=password)
    except ValidationError:
        st.toast(
            ":red[Такого пользователя не существует]",
            icon="❌"
        )
        return

    try:
        request = authentificate_user(login_data, password)

        if request.status_code == 200:

            cookie_manager.set(
                "user_access",
                request.text[1:-1]
            )

            st.toast(
                ":green[Пользователь успешно авторизован",
                icon="✅"
            )

            st.session_state['user_access'] = request.text[1:-1]

            right_rerun(st, cookie_manager)

        elif request.status_code == 401:
            st.toast(
                ":red[Такого пользователя не существует]",
                icon="❌"
            )

    except Exception:
        st.toast(
            ":yellow[При выполнении запроса произошла ошибка]",
            icon="⚠️"
        )
        return
