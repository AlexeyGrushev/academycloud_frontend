import pandas as pd
import streamlit

from streamlit_cookies_controller import CookieController

from src.utils.get_leaderboard import get_leaderboard
from src.utils.get_scoreboard import get_scoreboard
from src.utils.get_week_dates import get_week_dates


class LeaderBoardPage:
    def __init__(self, st: streamlit, cookie_manager: CookieController):
        self.st = st
        self.cookie_manager = cookie_manager
        self.markdown()
        pass

    def markdown(self):
        self.st.header("Таблица лидеров 🏆")
        self.st.markdown(
            '''
                <style>
                .st-emotion-cache-r421ms {
                    background-color: rgba(220, 220, 220, 0.3);
                }
                </style>
            ''',
            unsafe_allow_html=True
        )

        with self.st.container(border=True):
            self.st.subheader("Общий рейтинг.\nТоп 20")
            rating = get_leaderboard(
                token=self.cookie_manager.get("user_access"),
                limit=20,
                start_date=None,
                end_date=None
            )

            if rating:
                rating_data = [[
                    item[1], item[2], str(item[3]) + " ⭐️"
                ] for item in rating["data"]]
                rating_data.insert(0, [])

                rating_df = pd.DataFrame(rating_data, columns=(
                    "Имя", "Фамилия", "Количество очков"))
                rating_df = rating_df.iloc[1:]
                self.st.table(rating_df)

                main_scoreboard = get_scoreboard(
                    token=self.cookie_manager.get("user_access"),
                    start_date=None,
                    end_date=None
                )
                if not main_scoreboard:
                    main_scoreboard = "-"
                else:
                    main_scoreboard = main_scoreboard["position"]
                self.st.write(f"Вы на месте: {main_scoreboard}")

        with self.st.container(border=True):
            self.st.subheader("Недельный рейтинг.\nТоп 20")
            week_dates = get_week_dates()
            week_rating = get_leaderboard(
                token=self.cookie_manager.get("user_access"),
                limit=20,
                start_date=str(week_dates[0]),
                end_date=str(week_dates[1])
            )

            if week_rating:
                rating_data = [[
                    item[1], item[2], str(item[3]) + " ⭐️"
                ] for item in week_rating["data"]]
                rating_data.insert(0, [])

                rating_df = pd.DataFrame(rating_data, columns=(
                    "Имя", "Фамилия", "Количество oчков"))
                rating_df = rating_df.iloc[1:]
                self.st.table(rating_df)

                week_scoreboard = get_scoreboard(
                    token=self.cookie_manager.get("user_access"),
                    start_date=str(week_dates[0]),
                    end_date=str(week_dates[1])
                )
                if not week_scoreboard:
                    week_scoreboard = "-"
                else:
                    week_scoreboard = week_scoreboard["position"]

                self.st.write(f"Вы на месте: {week_scoreboard}")
