FROM python:3-alpine

MAINTAINER Aliaksei Kaliutau

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apk add --update \
  && pip install --upgrade pip  \
  && pip install -r requirements.txt \
  && rm -rf /var/cache/apk/*

COPY ./nanotwitter /app/nanotwitter
RUN ls /app/nanotwitter
RUN set FLASK_APP=/app/nanotwitter/wsgi.py 
RUN set FLASK_ENV=development

CMD flask run -h 0.0.0.0