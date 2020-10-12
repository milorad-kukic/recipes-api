FROM python:3.9.0-alpine

LABEL MAINTAINER "Milorad Kukic <kukic.milorad@gmail.com>"

ENV PYTHONUNBUFFERED 1

COPY ./app/requirements/ /requirements
RUN pip install -r /requirements/dev.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user


