FROM python:3.9

WORKDIR /home

ENV TELEGRAM_API_TOKEN="1653214808:AAEBtQbr0xuXFcaingH94vjplu-8x_1qVQE"
ENV TELEGRAM_ACCESS_ID="344928892,1596273768"

COPY ./pip_requirements.txt ./
RUN pip install -r ./pip_requirements.txt && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY ./handlers/*.py ./handlers/
COPY ./modules/*.py ./modules/
COPY createdb.sql ./
RUN mkdir /home/db

ENTRYPOINT ["python", "server.py"]

