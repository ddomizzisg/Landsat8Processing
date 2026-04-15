FROM ubuntu:22.04

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Capa 1: Actualización base y utilidades esenciales de red/sistema
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Capa 2: Herramientas de compilación y control de versiones
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Capa 3: Compiladores específicos (GCC 9) y configuración
# Útil si tu código requiere una versión de compilador antigua
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    apt-get update && apt-get install -y \
    gcc-9 \
    g++-9 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 \
    --slave /usr/bin/g++ g++ /usr/bin/g++-9 \
    --slave /usr/bin/gcov gcov /usr/bin/gcov-9 \
    && rm -rf /var/lib/apt/lists/*

# Capa 4: Dependencias de C++ y librerías de desarrollo
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    nlohmann-json3-dev \
    libssl-dev \
    libjsoncpp-dev \
    libicu-dev \
    libbz2-dev \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Capa 5: Entornos de ejecución (Python y Java)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Capa 6: Instalación de Docker Engine (CLI y herramientas)
RUN mkdir -p /usr/share/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io && \
    rm -rf /var/lib/apt/lists/*

# Capa 7: Docker Compose binario
RUN curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Capa 8: Compilación manual de CMake 3.21.2 (si la versión de apt no es suficiente)
WORKDIR /installation
RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2.tar.gz && \
    tar -xzvf cmake-3.21.2.tar.gz && \
    cd cmake-3.21.2 && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    cd .. && rm -rf cmake-3.21.2*

# Capa 9: Compilación manual de Boost 1.77.0
RUN wget -O boost_1_77_0.tar.gz https://sourceforge.net/projects/boost/files/boost/1.77.0/boost_1_77_0.tar.gz/download && \
    tar -xzvf boost_1_77_0.tar.gz && \
    cd boost_1_77_0 && \
    ./bootstrap.sh --prefix=/usr/ && \
    ./b2 -j$(nproc) install && \
    cd .. && rm -rf boost_1_77_0*

# Capa 10: Código de la aplicación
COPY ./app /home/app
WORKDIR /home/app/puzzlemesh

# Capa 11: Build final
RUN cmake . && make 

WORKDIR /home/app