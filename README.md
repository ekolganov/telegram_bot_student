В переменных окружения надо проставить API токен бота, а также адрес proxy и логин-пароль к ней.

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_ACCESS_ID` — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируются)

Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, в Dockerfile, а также в команде запуска укажите локальную директорию с проектом вместо `local_project_path`. SQLite база данных будет лежать в папке проекта `db/students.db`.

```
docker build -t tg_bot ./
docker run -d --name tg_bot_cont -v ./db:/home/db tg_bot
```

Чтобы войти в работающий контейнер:

```
docker exec -ti tg_bot_cont bash
```

Войти в контейнере в SQL шелл:

```
docker exec -ti tg_bot_cont bash
sqlite3 /home/db/students.db
```

Удобство отображения в sqlite
```
.mode column
.headers on
```

join
```
select st.*,th.theme_name from student st left join themes th on th.themes_grade_number=st.grade_number;
```