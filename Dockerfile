FROM python:3.9

WORKDIR /home

ENV TELEGRAM_API_TOKEN=""
#if wanna many access ids write: "123456,654321"
ENV TELEGRAM_ACCESS_ID=""

#set Moscow timezone
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./pip_requirements.txt ./
RUN pip install -r ./pip_requirements.txt && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY ./handlers/*.py ./handlers/
COPY ./modules/*.py ./modules/
COPY createdb.sql ./
RUN mkdir /home/db

ENTRYPOINT ["python", "server.py"]

