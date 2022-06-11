FROM python:3.9-slim

RUN apt update && apt install -y build-essential

WORKDIR /code
COPY ./app ./app
COPY ./migrations ./migrations
COPY ./gunicorn.conf.py ./
COPY ./wsgi_app.py ./
COPY ./entrypoint.sh ./
COPY ./requirements.txt ./

RUN chmod u+x ./entrypoint.sh
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt