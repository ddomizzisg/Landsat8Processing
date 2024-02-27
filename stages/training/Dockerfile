FROM python:3.7.6-buster

WORKDIR /installation
ADD requirements.txt /installation
RUN pip install -r requirements.txt

ADD app /app
ADD API /API

WORKDIR /code

EXPOSE 5000
ENTRYPOINT [ "python3", "/API/main.py" ]
