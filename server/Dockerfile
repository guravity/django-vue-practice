FROM python:3.9-slim-buster

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get clean

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .