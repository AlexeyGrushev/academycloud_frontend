import time
import streamlit as st

from PIL import Image
from streamlit_cookies_controller import CookieController

from pages.profile.schemas import SUpdateUser
from src.utils.config import settings
from src.utils.get_profile import get_user_profile
from src.utils.send_confirm_email import send_confirm_email
from src.utils.update_profile import update_user_profile
from src.utils.get_scoreboard import get_scoreboard
from src.utils.get_week_dates import get_week_dates
from src.utils.update_user import update_user
from utils.authentificate_user import authentificate_user
from utils.deactivate_user import deactivate_user


class ProfilePage:
    def __init__(self, st: st, cookie_manager: CookieController) -> None:
        self.st = st
        self.cookie_manager = cookie_manager
        self.markdown()
        pass

    def markdown(self):
        # self.st.markdown(
        #     '''
        #         <style>
        #         .st-emotion-cache-r421ms {
        #             background-color: rgba(220, 220, 220, 0.3);
        #         }
        #         </style>
        #     ''',
        #     unsafe_allow_html=True
        # )
        user = get_user_profile(self.cookie_manager.get("user_access"))

        self.st.header("Профиль")

        tab1, tab2 = st.tabs(["Информация о профиле", "Настройки"])

        with tab1:
            if user["profile_pic"]:
                self.st.image(
                    f"{settings.API_URL}/image/{user['profile_pic']}",
                    width=128
                )
            else:
                self.st.image(
                    f"{settings.API_URL}/image/profile_pic_default.jpeg",
                    width=128
                )
            self.st.header(f"{user['first_name']} {user['last_name']}")
            self.st.subheader(f"“{user["status"]}“")
            self.st.write(f"**ID пользователя:** {user["id"]}")
            self.st.write(f"**Логин:** {user["login"]}")
            email_verified = ":red[Не подтвержден]"
            if user["is_verified"]:
                email_verified = ":green[Подтвержден]"
            self.st.write(f"**Email:** {user["email"]} ({email_verified})")
            if user["is_verified"] is False:
                if self.st.button("Подтвердить Email"):
                    send_confirm_email(self.cookie_manager.get("user_access"))
                    self.st.toast(
                        ":blue[Ссылка с подтверждением"
                        " отправлена Вам на почту]",
                        icon="ℹ"
                    )

            with self.st.container(border=True):
                self.st.subheader("Сводка")
                col1m, col2m = self.st.columns(2)
                with col1m.container(border=True):
                    col1, col2 = self.st.columns(2)
                    with col1.container(border=True):
                        self.st.subheader("Уроков пройдено📚")
                        self.st.write(f"**{user["task_completed"]}**")
                    with col2.container(border=True):
                        self.st.subheader("Очков заработано⭐️")
                        self.st.write(f"**{user["points"]}**")

                with col2m.container(border=True):
                    col1, col2 = self.st.columns(2)

                    main_scoreboard = get_scoreboard(
                        token=self.cookie_manager.get("user_access"),
                        start_date=None,
                        end_date=None
                    )
                    if not main_scoreboard:
                        main_scoreboard = "-"
                    else:
                        main_scoreboard = main_scoreboard["position"]

                    start_date, end_date = get_week_dates()
                    week_scoreboard = get_scoreboard(
                        token=self.cookie_manager.get("user_access"),
                        start_date=str(start_date),
                        end_date=str(end_date)
                    )
                    if not week_scoreboard:
                        week_scoreboard = "-"
                    else:
                        week_scoreboard = week_scoreboard["position"]

                    with col1.container(border=True):
                        self.st.subheader("Место в рейтинге📈")
                        self.st.write(f"**№ {main_scoreboard}**")
                    with col2.container(border=True):
                        self.st.subheader("Недельный рейтинг📈")
                        self.st.write(f"**№ {week_scoreboard}**")

        with tab2:
            with self.st.container(border=True):
                self.st.subheader("Настройки профиля")
                col1, col2 = self.st.columns(2)

                image = None

                try:
                    image_view = col1.empty()

                    image_view.image(
                        f"{settings.API_URL}/image/profile_pic_default.jpeg",
                        width=150
                    )
                except Exception:
                    col1.text("Кажется что-то пошло не так🤔")

                profile_pic = col2.file_uploader(
                    "Загрузите изображение профиля",
                    type=["png", "jpg", "jpeg"],
                )
                col2.text(
                    "Самый идеальный размер изображения составляет 150x150 px."
                )

                first_name = self.st.text_input(
                    "Имя *", value=user["first_name"])
                last_name = self.st.text_input(
                    "Фамилия *",  value=user["last_name"])
                status = self.st.text_area(
                    "Статус профиля", max_chars=200,  value=user["status"])

                self.st.text("* Обязательно для заполнения")

                submit_btn = self.st.button("Обновить профиль")

                if profile_pic:
                    image = Image.open(profile_pic).resize(
                        (150, 150)
                    )
                    image_view.image(
                        image,
                        width=150
                    )

                if submit_btn:
                    update_user_profile(
                        self.st,
                        self.cookie_manager,
                        first_name.replace(" ", ""),
                        last_name.replace(" ", ""),
                        status,
                        profile_pic
                    )

            with self.st.container(border=True):
                self.st.subheader("Задать новый пароль")

                old_pass = self.st.text_input(
                    "Старый пароль", type="password")
                new_pass = self.st.text_input(
                    "Новый пароль", type="password")
                retry_new_pass = self.st.text_input(
                    "Повторите новый пароль", type="password")

                if self.st.button("Обновить пароль"):
                    if new_pass == retry_new_pass:
                        try:
                            update_user(
                                st=self.st,
                                cookie_manager=self.cookie_manager,
                                login_data=user["login"],
                                password=old_pass,
                                data=SUpdateUser(password=new_pass)
                            )
                        except Exception:
                            self.st.toast(
                                ":red[Пароль должен быть не менее 8 символов]",
                                icon="❌"
                            )
                    else:
                        self.st.toast(
                            ":red[Пароли не совпадают]",
                            icon="❌"
                        )
            with self.st.container(border=True):
                self.st.subheader("Сменить Email")

                old_pass = self.st.text_input(
                    "Пароль", type="password")
                email = self.st.text_input(
                    "Новый Email")

                if self.st.button("Изменить Email"):
                    try:
                        update_user(
                            st=self.st,
                            cookie_manager=self.cookie_manager,
                            login_data=user["login"],
                            password=old_pass,
                            data=SUpdateUser(email=email)
                        )
                    except Exception:
                        self.st.toast(
                            ":red[Вы ввели не Email]",
                            icon="❌"
                        )

            with self.st.container(border=True):
                self.st.subheader(":red[Декативация учётной записи]")

                password = self.st.text_input(
                    "Парoль", type="password"
                )

                control_phrase = self.st.text_input(
                    "Введите фразу: “:red[Да, я хочу деактивировать"
                    " свою учётную запись]“"
                )

                if self.st.button(":red[Деактивировать]"):
                    if control_phrase == "Да, я хочу" \
                            " деактивировать свою учётную запись":
                        response = authentificate_user(user["login"], password)
                        if response.status_code == 200:
                            if deactivate_user(
                                    self.cookie_manager.get("user_access")):
                                self.st.toast(
                                    ":blue[Ваша учётная"
                                    " запись деактивирована]",
                                    icon="ℹ"
                                )
                                time.sleep(2)
                                self.st.rerun()
                        else:
                            self.st.toast(
                                ":red[Пароль введен неверно]",
                                icon="❌"
                            )
                    else:
                        self.st.toast(
                            ":red[Контрольная фраза введена неверно]",
                            icon="❌"
                        )
