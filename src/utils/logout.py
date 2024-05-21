import streamlit
from streamlit_cookies_controller import CookieController

from src.utils.right_rerun import right_rerun


def logout(st: streamlit, cookie_manager: CookieController):
    try:
        cookie_manager.remove("user_access")
        try:
            cookie_manager.remove("last_lesson_result")
        except Exception:
            pass
        right_rerun(st, cookie_manager)
    except Exception:
        pass
