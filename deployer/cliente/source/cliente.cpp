#include "cliente.h"

bool Cliente::connect_to_master()
{
    // Crear socket
    if ((this->sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("Error al crear el socket");
        return false;
    }

    this->server_addr.sin_family = AF_INET;
    this->server_addr.sin_port = htons(this->port);
    inet_pton(AF_INET, this->server_ip.c_str(), &this->server_addr.sin_addr);

    // Conectar al servidor
    if (connect(this->sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1)
    {
        perror("Error al conectar con el servidor");
        close(this->sockfd);
        return false;
    }

    return true;
}

bool Cliente::close_conn()
{
    close(sockfd);
}

void Cliente::run()
{
    this->keep_execution = true;

    while(this->keep_execution)
    {
        // Recibir comando del servidor
        memset(this->buffer, 0, BUFFER_SIZE);
        if (recv(this->sockfd, this->buffer, BUFFER_SIZE, 0) <= 0) {
            perror("Error al recibir datos");
            close(sockfd);
            break;
        }

        std::cout << "Comando recibido: " << buffer << std::endl;
    }
}

bool Cliente::execute_cmd(string cmd)
{
    return false;
}