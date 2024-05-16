import streamlit as st

from streamlit_cookies_controller import CookieController

from src.utils.get_items import get_items
from src.utils.get_lessons import get_lessons
from utils.right_rerun import right_rerun


class TaskCatalog:
    def __init__(self, st: st, cookie_manager: CookieController) -> None:
        self.st = st
        self.cookie_manager = cookie_manager
        self.markdown()
        pass

    def markdown(self):
        self.st.header("Каталог заданий")

        items = get_items(self.cookie_manager)

        if not items:
            self.st.toast(
                ":yellow[При выполнении запроса произошла ошибка]",
                icon="⚠️"
            )
            return
        else:
            options = list(items.keys())

        item_selectbox = self.st.selectbox(
            "Выберите предмет",
            options, format_func=lambda x: items[x])

        lessons = get_lessons(
            item_id=item_selectbox,
            cookie_manager=self.cookie_manager)

        if lessons == {}:
            self.st.subheader(
                "По этому предмету заданий пока нет,"
                " но они обязательно появятся...")

        self.st.markdown(
            '''
        <style>
        .eqpbllx5 {
            background-color: rgba(220, 220, 220, 0.3);
        }
        </style>
    ''',
            unsafe_allow_html=True
        )

        for key, value in lessons.items():
            # Создаем контейнер с рамкой
            with st.expander(f"**{value['name']}**", expanded=True):
                # Отображаем информацию о тесте
                st.write(f"Автор: {value['owner']}")
                st.write(f"Награда: до {value['reward']} ⭐️")
                st.write(
                    f"Количество заданий: {value['number_of_questions']}"
                )

                # Добавляем кнопку "Начать"
                if st.button(f"Начать выполнение ID: {key}"):
                    self.cookie_manager.set("lesson_id", str(key))
                    right_rerun(self.st, self.cookie_manager)
