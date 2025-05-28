#ifndef CLIENTE_H
#define CLIENTE_H

#include <iostream>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string>

using namespace std;
#define BUFFER_SIZE 1024

class Cliente
{
private:
    int sockfd;
    struct sockaddr_in server_addr;
    string server_ip;
    int port;
    bool keep_execution;
    char buffer[BUFFER_SIZE];
public:

    Cliente(){};
    Cliente(string server_ip, int server_port){
        this->server_ip = server_ip;
        this->port = server_port;
    };

    bool connect_to_master();
    bool close_conn();
    void run();
    bool execute_cmd(string cmd);
};

#endif