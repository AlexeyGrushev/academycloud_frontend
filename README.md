# Academy Cloud Frontend (Streamlit)
Pet-проект: Система обучения по учебным дисциплинам Academy Cloud (FrontEnd)

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Команда проекта](#команда-проекта)
- [Источники](#источники)

## Технологии
Для разработки был использован следующий стек:
- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Streamlit](https://streamlit.io/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- streamlit-option-menu
- streamlit-cookies-controller

## Использование
Для использования проекта необходимо:

Убедиться в наличии пакетного менеджера **Poetry**:
```sh
$ poetry --version
```

Окрыть папку проекта в терминале

Установить все зависимости :
```sh
$ poetry install
```

Клонировать файл окружения и задать их значения:
```sh
$ cat env_sample > .env
```

После чего можем запустить прокет командой:
```sh
poetry run python3 -m streamlit run src/app.py --server.address 0.0.0.0
```

## Deploy и CI/CD
Для развертки на сервере потребуется настроить [NGINX](https://nginx.org/en/)


### Зачем был разработан этот проект?
Проект изначально был создан как Pet, но позже был использован для защиты выпускной квалификационной работы.


## Команда проекта
- [Алексндр](https://t.me/grushev_works) — Основной разработчик

## Источники
Источниками вдохновения стали: мой предыдуший проект ([Математический тренажер Math](https://github.com/AlexeyGrushev/math_course_work)), сервисы по типу Skillbox, Getbrains, Duolingo. <br>
Для запуска проета потребуется его Back-end часть проекта, которую можно отыскать [здесь]("https://github.com/AlexeyGrushev/academycloud_backend")