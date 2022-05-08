FROM ubuntu:18.04

# ARG DEBIAN_FRONTEND=noninteractive
# 
# RUN apt-get remove docker docker-engine docker.io containerd runc
# 
# RUN apt-get update
# 
# RUN apt-get -y install \
#     ca-certificates \
#     curl \
#     gnupg \
#     lsb-release \
#     git
#     
# RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# 
# RUN echo \
#   "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
#   
# RUN apt-get update
# 
# RUN apt-get install -y golang-github-docker-containerd-dev
# RUN apt-get install -y docker-ce docker-ce-cli containerd.

RUN apt-get update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt install -y gcc-9 g++-9
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9 --slave /usr/bin/gcov gcov /usr/bin/gcov-9
RUN update-alternatives --config gcc
RUN apt-get install -y make
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y nlohmann-json-dev
RUN apt-get install -y wget curl
RUN apt-get install -y default-jdk
RUN apt-get install -y libssl-dev
RUN apt-get install -y python3 python3-pip


RUN apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt -y install nodejs

RUN pip3 install mysql-connector-python


#RUN apt-get install -y python-pip
#RUN pip install statistics
RUN curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN apt-get install  -y python3-pip
RUN apt-get install -y python-dev autotools-dev libicu-dev libbz2-dev libboost-all-dev

WORKDIR /installation

RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2.tar.gz
RUN tar -xzvf cmake-3.21.2.tar.gz
WORKDIR /installation/cmake-3.21.2
RUN ./configure
RUN make
RUN make install

WORKDIR /installation

RUN wget -O boost_1_77_0.tar.gz https://sourceforge.net/projects/boost/files/boost/1.77.0/boost_1_77_0.tar.gz/download
RUN tar -xzvf boost_1_77_0.tar.gz

WORKDIR /installation/boost_1_77_0


RUN ./bootstrap.sh --prefix=/usr/
RUN ./b2
RUN ./b2 install

# WORKDIR /home/app/deployer
# RUN make clean
# RUN make
# ommited since there is no source code to compile
# RUN make clean
# RUN make

COPY ./source /home/app

RUN apt-get install -y libjsoncpp-dev
WORKDIR /home/app
RUN make


WORKDIR /home/app
RUN pip3 install --no-cache-dir -r requirements.txt


