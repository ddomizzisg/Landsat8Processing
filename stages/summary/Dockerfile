FROM ghcr.io/osgeo/gdal:ubuntu-full-latest
RUN apt-get update

RUN apt-get install -y python3 python3-pip

#install requeriments
COPY requirements.txt /installation/requirements.txt
RUN pip3 install -r /installation/requirements.txt --break-system-packages


COPY app /app

WORKDIR /app
RUN mkdir /inputs
RUN mkdir /outputs
#export dependencies


ADD ./API /API
WORKDIR  /API
RUN apt-get install -y curl

EXPOSE 5000
ENTRYPOINT [ "python3", "/API/main.py" ]
