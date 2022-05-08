FROM python:3.10-buster

RUN apt-get update
ENV GOOGLE_KEY='AIzaSyD6ecliaEzPAeolaKjSwswOkxIIGTQxKw4'

WORKDIR /app
ADD code /app

COPY requirements.txt /installation/requirements.txt
RUN pip install -r /installation/requirements.txt

ADD ./API /API
WORKDIR  /API

RUN apt-get install -y curl
RUN apt-get install python3-psycopg2

EXPOSE 5000
ENTRYPOINT [ "python3", "/API/main.py" ]
