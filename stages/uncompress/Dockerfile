FROM ddomizzi/lz4:v1

RUN apt-get update
RUN apt-get install -y python3 python3-pip

WORKDIR /installation
ADD requirements.txt /installation
RUN pip3 install -r requirements.txt

ADD API /API

WORKDIR /code

EXPOSE 5000
ENTRYPOINT [ "python3", "/API/main.py" ]