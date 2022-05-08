FROM consbio/python3.6-gdal2:latest
RUN apt-get update

#install requeriments
COPY requirements.txt /installation/requirements.txt
RUN pip install -r /installation/requirements.txt

RUN pip uninstall gdal -y
RUN pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
COPY app /app

WORKDIR /app
RUN mkdir /inputs
RUN mkdir /outputs
#export dependencies
#RUN export PYTHONPATH=/app/GDAL_Python3
RUN PYTHONPATH="/app/GDAL_Python3"

ADD ./API /API
WORKDIR  /API
RUN apt-get install -y curl

EXPOSE 5000
ENTRYPOINT [ "python3", "/API/main.py" ]
