from datetime import datetime, timedelta, timezone


def get_week_dates():
    # Получение текущей даты и времени в UTC
    now = datetime.now(timezone.utc)

    # Вычисление даты начала недели (понедельник)
    start_of_week = now - timedelta(days=now.weekday())

    # Вычисление даты конца недели (воскресенье)
    end_of_week = start_of_week + timedelta(days=7)

    # Возвращение дат начала и конца недели
    return start_of_week.date(), end_of_week.date()
