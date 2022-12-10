FROM python:3.8.3-alpine



ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /manage/manage_1/manage_2/docke
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
#WORKDIR /manage/manage_1/manage_2/docker
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev
#ENV PYTHONUNBUFFERED 1
#
#COPY Pipfile .
#COPY Pipfile.lock .
#RUN pip install pipenv
#RUN pipenv install  --deploy --ignore-Pipfile
#
#COPY . .