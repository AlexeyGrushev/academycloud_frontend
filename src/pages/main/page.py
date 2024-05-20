import json
import streamlit as st

from random import choice
from datetime import datetime, timedelta, timezone

from streamlit_cookies_controller import CookieController

from src.utils.get_profile import get_user_profile
from src.utils.get_scoreboard import get_scoreboard
from src.utils.send_confirm_email import send_confirm_email
from src.utils.get_items import get_items
from src.utils.get_lessons import get_lessons
from src.utils.right_rerun import right_rerun
from src.utils.get_lesson import get_lesson


class MainPage:
    def __init__(self, st: st, cookie_manager: CookieController) -> None:
        self.st = st
        self.cookie_manager = cookie_manager
        self.markdown()
        pass

    def markdown(self):
        user = get_user_profile(self.cookie_manager.get("user_access"))

        header_col1, header_col2 = self.st.columns(2)

        header_col1.image("src/static/img/logo.png")

        header_col2.header(f"Здравствуйте, :blue[{user["first_name"]}]")
        header_col2.subheader("Вперед к получению знаний!")

        with self.st.container(border=True):
            today_score = get_scoreboard(
                token=self.cookie_manager.get("user_access"),
                start_date=str(datetime.now(timezone.utc).date()),
                end_date=str((datetime.now(
                    timezone.utc) + timedelta(days=1)).date())
            )
            if today_score:
                self.st.subheader(
                    "За сегодня Вы заработали "
                    f":blue[{today_score['points']}] ⭐️"
                )
            else:
                self.st.subheader(
                    "Сегодня Вы ещё не занимались."
                    " Пройдите урок прямо сейчас!")

        if user["is_verified"] is False:
            self.st.info(
                "Защитите свою учётную запись, "
                "подтвердив адрес электронной почты")
            if self.st.button("Подтвердить почту"):
                send_confirm_email(self.cookie_manager.get("user_access"))
                self.st.toast(
                    ":blue[Ссылка с подтверждением"
                    " отправлена Вам на почту]",
                    icon="ℹ"
                )

        if self.cookie_manager.get("last_lesson_result"):
            try:
                to_dict = str(self.cookie_manager.get("last_lesson_result"))
                last_lesson_answers = json.loads(
                    to_dict.replace(
                        "'", '"'))
                last_lesson_data = get_lesson(
                    int(last_lesson_answers["lesson_id"]),
                    self.cookie_manager
                )

                last_lesson_text = \
                    f"Вы завершили занятие:" \
                    f" :blue[{last_lesson_data['name']}]  \n" \
                    "За выполнение заработали:" \
                    f" :blue[{last_lesson_answers['reward']}] ⭐️   \n" \
                    "Ответы:  \n"

                for i in range(len(last_lesson_answers["correct_answers"])):
                    if last_lesson_answers["correct_answers"][i] == 1:
                        last_lesson_text += f"{i + 1}: ✅  \n"
                    else:
                        last_lesson_text += f"{i + 1}: ❌  \n"

                self.st.info(last_lesson_text)
            except Exception:
                self.cookie_manager.remove("last_lesson_result")
                pass

        with self.st.container(border=True):
            iteration = 0
            while iteration < 50:
                iteration += 1
                items = get_items(self.cookie_manager)
                lessons = get_lessons(
                    choice(list(items)),
                    self.cookie_manager
                )
                if lessons == {}:
                    continue
                else:
                    lesson_id = choice(list(lessons))
                    break
            self.st.subheader(
                "Начните проходить случайное занятие")
            if self.st.button("Начать случайное занятие"):
                self.cookie_manager.set("lesson_id", lesson_id)
                right_rerun(self.st, self.cookie_manager)

        with self.st.container(border=True):
            self.st.subheader(
                "Или выберите подходящее задание из :blue[Каталога заданий]")
