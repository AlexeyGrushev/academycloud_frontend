import streamlit

from streamlit_cookies_controller import CookieController

from src.pages.lesson.lesson_test_page import LessonTestPage
from src.utils.get_lesson import get_lesson
from src.utils.right_rerun import right_rerun


class LessonDistributorPage:
    def __init__(self, st: streamlit, cookie_manager: CookieController):
        self.st = st
        self.cookie_manager = cookie_manager
        self.distributor()
        pass

    def distributor(self):
        lesson_data = get_lesson(
            lesson_id=self.cookie_manager.get("lesson_id"),
            cookie_manager=self.cookie_manager
        )

        if not lesson_data:
            self.cookie_manager.remove("lesson_id")
            right_rerun(self.st, self.cookie_manager)

        if lesson_data["type"] == "test":
            LessonTestPage(self.st, self.cookie_manager, lesson_data)
