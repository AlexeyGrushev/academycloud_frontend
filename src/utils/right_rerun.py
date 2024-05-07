import time
import streamlit

from streamlit_cookies_controller import CookieController


def right_rerun(st: streamlit, cookie_manager: CookieController):
    if 'cookies' not in st.session_state:
        st.session_state['cookies'] = False

    time.sleep(.5)

    st.session_state['cookies'] = cookie_manager.getAll()

    st.rerun()
