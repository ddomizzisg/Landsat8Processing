FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

ARG DEBIAN_FRONTEND=noninteractive


RUN apt-get update

ENV GOOGLE_KEY='AIzaSyD6ecliaEzPAeolaKjSwswOkxIIGTQxKw4'

RUN apt-get install -y python3 python3-pip

#RUN pip uninstall gdal -y --break-system-packages
#RUN pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal" --break-system-packages

WORKDIR /apps
ADD apps /apps

RUN pip install -r /apps/requirements.txt --break-system-packages

RUN apt-get install -y python3-psycopg2


RUN PYTHONPATH="/app/GDAL_Python3"

RUN pip3 install pymongo globus-compute-endpoint --break-system-packages

WORKDIR /parsltests