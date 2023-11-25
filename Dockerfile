# Dockerfile

FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app


COPY requirements.txt /app/
COPY mod_wsgi-4.9.2-cp39-cp39-win_amd64.whl /app/

RUN dir

RUN pip install --upgrade pip && pip install -r requirements.txt