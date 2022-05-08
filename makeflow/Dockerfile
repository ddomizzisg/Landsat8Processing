FROM ddomizzi/lz4

RUN apt-get update
RUN apt-get install -y git build-essential zlib1g-dev
RUN apt-get install -y python python-dev python-pip

WORKDIR /home/makeflow

RUN git clone https://github.com/cooperative-computing-lab/cctools cctools-source

WORKDIR /home/makeflow/cctools-source

RUN ./configure

RUN make

RUN mkdir doc/man/html

RUN make install

ENV PATH="$PATH:/home/makeflow/cctools-source/makeflow/src"
ENV PYVER="$(python -c 'import sys; print("%s.%s" % sys.version_info[:2])')"
ENV PYTHONPATH="${PYTHONPATH}:${HOME}/cctools/lib/python${PYVER}/site-packages"

RUN apt-get install -y curl nano 

RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

RUN  apt-get update

RUN  apt-get install -y docker-ce docker-ce-cli containerd.io
