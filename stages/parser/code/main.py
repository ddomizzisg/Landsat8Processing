# -*- coding: utf-8 -*-
#!/usr/bin/env python

from os import listdir
from os.path import isfile, join, isdir
import urllib, json, sys,time,re,codecs
import time
import socket
import logging
import os
import struct
import traceback
import json
#Importing all from thread
from thread import *
from pymongo import MongoClient

#clases
from lugar import Lugar
from database import DataBase
from parser_lansat import ParserLansat
from parser_landsat5 import ParserLansat5
from parser_landsat8 import ParserLansat8
from parser_1 import ParserUno
from latlng_to_pathrow import ConvertToWRS


#obtiene los archivos del directorio especificado
def getDirectories(path):
    return [f for f in listdir(path) if isdir(join(path, f))]

def getFiles(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


#guarda la estructura generada en un archivo JSON
def saveToJson(lst,path):
    print(json.dumps(lst, ensure_ascii=False, indent=2))
    #with  codecs.open('_{}'.format(path), 'w', encoding="utf-8") as outfile:
     #   json.dump(lst, outfile, ensure_ascii=True, indent=4)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    #logger.info('entro aqui')
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

#send message by socket
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def clientthread(conn):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Client connected')
    
    recibido = recv_msg(conn)
    
    logger.info('data received ')
    #logger.info('Received %s',recibido)
    data = json.loads(recibido)
    result = ""
    if(data['filename'][:3] == "CMA" or data['filename'] == "CMT"):
        f = ParserUno(data['content'], data['filename'],db, data['usrToken'], data['catalog'])
        try:
            result = f.parse()
        except Exception as e:
            logger.info("ERROR"+str(e))
            logger.info(traceback.format_exc())
            print(str(e))
        del f
    elif(data['filename'][:3] == "CHM"):
            f = ParserLansat(data['content'], data['filename'],db, data['usrToken'], data['catalog'])
            try:
                result = f.parse()
            except Exception as e:
                logger.info("ERROR"+str(e))
                logger.info(traceback.format_exc())
                print(str(e))
            del f
    elif(data['filename'][:4] == "LT05"):
        f = ParserLansat5(data['content'], data['filename'],db, data['usrToken'], data['catalog'])
        try:
            result = f.parse()
        except Exception as e:
            logger.info("ERROR"+str(e))
            logger.info(traceback.format_exc())
            print(str(e))
        del f
    elif(data['filename'][:4] == "LC08"):
        logger.info('Aquiiiii')
        f = ParserLansat8(data['content'], data['filename'],db, data['usrToken'], data['catalog'])
        try:
            result = f.parse()
        except Exception as e:
            logger.info("ERROR"+str(e))
            logger.info(traceback.format_exc())
            print(str(e))
        del f
        
    logger.info('Resultxxx %s', result)
    strJson = json.dumps(result, ensure_ascii=True, indent=2)
    send_msg(conn, strJson)
    #conn.close();
    logger.info('Server disconnected')


#main
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(os.environ["MONGO_DB"])
client = MongoClient(os.environ["MONGO_DB"], 27017)
db = client.placesCollection
logger.info("Connected to Mongo database %s",os.environ["MONGO_DB"])

path = "/home/metadata/"
con = ConvertToWRS()


#instanciamos un objeto para trabajar con el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Con el metodo bind le indicamos que puerto debe escuchar y de que servidor esperar conexiones
#Es mejor dejarlo en blanco para recibir conexiones externas si es nuestro caso
s.bind(("", int(os.environ["SOCKET_PORT"])))

#Aceptamos conexiones entrantes con el metodo listen, y ademas aplicamos como parametro
#El numero de conexiones entrantes que vamos a aceptar
s.listen(5)

#Instanciamos un objeto sc (socket cliente) para recibir datos, al recibir datos este 
#devolvera tambien un objeto que representa una tupla con los datos de conexion: IP y puerto
print "Listening on port " + os.environ["SOCKET_PORT"]
logger.info('Socket listening on port %s', os.environ["SOCKET_PORT"])
logging.warning('Listening')

lotTime = 0
while True:
    sc, addr = s.accept()
    start_new_thread(clientthread,(sc,))
    
s.close()


    
