FROM python:3.8.3-alpine


RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev

WORKDIR /manage/manage_1/manage_2/docker

ENV PYTHONUNBUFFERED 1


RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
COPY . .