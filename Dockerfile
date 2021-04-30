FROM python:3.8

WORKDIR /home
#1198928422
ENV TELEGRAM_API_TOKEN="1736892712:AAHDtOBkXm8t8xjgRnCMb8qfT3ZZuAG4QzY"
ENV TELEGRAM_ACCESS_ID=[344928892]

RUN pip install -U pip aiogram && apt-get update && apt-get install sqlite3 && apt-get install nano
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "server.py"]

