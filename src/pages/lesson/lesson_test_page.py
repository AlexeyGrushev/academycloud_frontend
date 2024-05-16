import json
import time
import streamlit

from streamlit_option_menu import option_menu
from streamlit_cookies_controller import CookieController

from src.utils.right_rerun import right_rerun
from utils.confirm_answers import confirm_answers


class LessonTestPage:
    def __init__(
            self,
            st: streamlit,
            cookie_manager: CookieController,
            lesson_data: dict):
        self.st = st
        self.cookie_manager = cookie_manager
        self.lesson_data = lesson_data
        self.markdown()
        pass

    def sidebar_nav_menu(self):
        question_num = 1
        tasks = []
        for i in self.lesson_data["body"]["questions"]:
            tasks.append(f"{question_num}. {i["question"]}")
            question_num += 1
        with self.st.sidebar:
            option = option_menu(
                menu_title="Задания",
                options=tasks,
                styles={"container": {
                    "background-color": 'rgba(240, 242, 246, 0);',
                    "padding": "7% 0% !important;",
                },
                }
            )
        return option

    def get_answer_list_from_cookie(self) -> list:
        answers_str = self.cookie_manager.get("lesson_answers")
        try:
            answers_list = json.loads(
                str(answers_str).replace("None", "null")
            )
            return answers_list
        except Exception:
            return [None]

    def markdown(self):
        if (self.cookie_manager.get("lesson_answers") is None or
            len(self.get_answer_list_from_cookie()) != len(
                self.lesson_data["body"]["questions"]
        )):
            self.cookie_manager.set(
                "lesson_answers",
                str([None for _ in self.lesson_data["body"]["questions"]])
            )

        self.st.sidebar.title("Тестирование")
        self.st.sidebar.header(self.lesson_data["name"])

        col1, col2 = self.st.sidebar.columns(2)

        if col1.button("Выйти❌"):
            self.cookie_manager.remove("lesson_id")
            self.cookie_manager.remove("lesson_answers")
            time.sleep(.5)
            right_rerun(self.st, self.cookie_manager)

        if col2.button("Завершить🏁"):
            answer_list = self.get_answer_list_from_cookie()
            if None in answer_list:
                self.st.toast(
                    ":red[Необходимо ответить на все вопросы]",
                    icon="❌"
                )
            else:
                data_to_send = []
                for i in range(
                        len(self.lesson_data["body"]["questions"])):
                    data_to_send.append(
                        self.lesson_data[
                            "body"]["questions"][i]["options"][answer_list[i]]
                    )
                result = confirm_answers(
                    lesson_id=self.cookie_manager.get("lesson_id"),
                    data_to_send=data_to_send,
                    cookie_manager=self.cookie_manager
                )
                if result:
                    result_info = \
                        "Задание завершено  \n" + \
                        f"Заработано: {result["reward"]} ⭐️  \n" + \
                        "Правильные ответы:  \n"

                    for i in range(len(result["correct_answers"])):
                        if result["correct_answers"][i] == 1:
                            result_info += f"{i + 1}: ✅  \n"
                        else:
                            result_info += f"{i + 1}: ❌  \n"

                    result_info += "Нажмите на любую из кнопок" + \
                        " чтобы покинуть задание"

                    self.st.sidebar.info(result_info)

                    time.sleep(.5)
                    self.cookie_manager.set("last_lesson_result", str(result))
                    self.cookie_manager.remove("lesson_id")
                    self.cookie_manager.remove("lesson_answers")

                    return

        question_nav_menu = self.sidebar_nav_menu()

        question_index = int(str(question_nav_menu).split(".")[0]) - 1

        question = dict(self.lesson_data["body"]["questions"][question_index])

        self.st.title(question["question"])

        answer = self.st.radio(
            "Выберите вариант ответа",
            options=question["options"],
            index=self.get_answer_list_from_cookie()[question_index]
        )

        if answer:
            answer_list = self.get_answer_list_from_cookie()
            answer_list[question_index] = question["options"].index(answer)
            self.cookie_manager.set("lesson_answers", str(answer_list))
            self.st.toast(
                ":blue[Ответ записан]",
                icon="ℹ"
            )
