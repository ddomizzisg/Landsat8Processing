FROM ubuntu:22.04

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip gcc

# Add API
ADD ./API /API
WORKDIR  /API
RUN pip3 install -r requirements.txt

# Add Load Balancer
ADD app /app
WORKDIR /app

ENTRYPOINT [ "python3", "/API/main.py" ]
