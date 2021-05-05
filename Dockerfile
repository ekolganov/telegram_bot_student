FROM python:3.9

WORKDIR /home
#1198928422
ENV TELEGRAM_API_TOKEN="1736892712:AAHDtOBkXm8t8xjgRnCMb8qfT3ZZuAG4QzY"
ENV TELEGRAM_ACCESS_ID=[344928892]

COPY ./pip_requirements.txt ./
# RUN pip install -U pip aiogram && apt-get update && apt-get install sqlite3 && apt-get install nano
RUN pip install -r ./pip_requirements.txt && apt-get update && apt-get install sqlite3 && apt-get install nano
COPY *.py ./
COPY ./handlers/*.py ./handlers/
COPY ./modules/*.py ./modules/
COPY createdb.sql ./
RUN mkdir /home/db

ENTRYPOINT ["python", "server.py"]

