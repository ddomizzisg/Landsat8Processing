FROM python:3.10

RUN apt-get update

WORKDIR /app

ADD requirements.txt /app/
ADD main.py /app

RUN pip install -r requirements.txt


