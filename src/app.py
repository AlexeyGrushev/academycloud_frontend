import streamlit as st

from src.static.styles import (
    hide_streamlit_style,
    set_page_background
)
from src.pages.auth.page import AuthPage
from src.pages.home.page import RootPage
from src.utils.get_profile import get_user_profile
from src.utils.cookies import get_manager


try:
    st.set_page_config(
        page_title="Academy Cloud",
        page_icon="☁️",
        layout="wide"
    )
except Exception:
    pass


class Application:
    def __init__(self) -> None:
        self.st = st
        self.cookie_manager = get_manager()
        self.launch()
        pass

    def launch(self):

        self.st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        self.st.markdown(set_page_background, unsafe_allow_html=True)

        auth = get_user_profile(self.cookie_manager.get("user_access"))

        if 'cookies' not in st.session_state:
            self.st.session_state['cookies'] = False

        if self.st.session_state['cookies']:
            cookies = self.st.session_state['cookies']
            for key in cookies:
                if (key == "_streamlit_xsrf" or key == "ajs_anonymous_id"):
                    continue
                elif key == "last_lesson_result":
                    self.cookie_manager.set(
                        key,
                        cookies[key],
                        max_age=60
                    )
                else:
                    self.cookie_manager.set(
                        key,
                        cookies[key],
                        max_age=60*60*24*30
                    )

        if not auth:
            AuthPage(self.st, self.cookie_manager)
        else:
            RootPage(self.st, self.cookie_manager)


def main():
    Application()


if __name__ == "__main__":
    main()
