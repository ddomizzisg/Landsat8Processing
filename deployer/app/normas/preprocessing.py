import yaml #pip install pyyaml
import json
import re

END_BLOCK_TAG = "[END]"
ASSIGNMENT_TAG = "="

"""
    Lee el archivo .yml utilizando la biblioteca yaml, retorna el contenido del archivo como objeto
"""
def read_yml_file(path):
    if not ".yml" in path.lower():
        return
    try:
        with open(path, encoding='utf-8') as f: #leer archivo
            data_content = f.read() #obtener contenido del archivo
    except Exception as inst:
        print(f"{inst}")
        return
    return yaml.load(data_content, Loader=yaml.FullLoader)
        

"""
    Lee el archivo .json de la configuración y lo retorna como objeto
"""
def read_json_file(path):
    if not ".json" in path.lower():
        print("AAA")
        return
    try:
        with open(path, encoding='utf-8') as f: #leer archivo
            data_content = f.read() #obtener contenido del archivo
    except Exception as inst:
        print(f"{inst}")
        return
    return json.loads(data_content) #decodificar json

"""
    Dado una ubicacion de un finchero .cfg, obtiene la configuracion inicial del archivo .cfg y retorna toda la informacion como un diccionario
"""
def read_cfg_file(path):
    if not ".cfg" in path.lower():
        return

    re_blockname = re.compile(r'\[.+\]') #obtiene el nombre del bloque
    re_atributes = re.compile(r'.+=.*') #obtiene la lista de los atributos del bloque, atributo = valor

    cfg = {} #diccionario del archivo
    
    current_blockdata = {} #se crea un diccionario que contendrá todos los pares: "atributo=valor" del bloque
    current_blockname = ""
    try :
        with open(path, encoding='utf-8') as f:
            for line in f:
                if END_BLOCK_TAG in line: # se identifico el final de un bloque
                    if current_blockname: #se identifico un bloque
                        if current_blockname not in cfg: #si la clave del bloque no esta en cfg, crear un arreglo
                            cfg[current_blockname] = []
                        cfg[current_blockname].append(current_blockdata) #agregar la informacion del bloque
                        current_blockdata = {}
                        current_blockname = ""
                else:
                    line = line.replace("\"", "\'")
                    attribute = re_atributes.findall(line) # se intanta identificar un atributo
                    if attribute: # se identifico un atributo
                        attribute_value = attribute[0].split(ASSIGNMENT_TAG)
                        current_blockdata[attribute_value[0].strip()] = attribute_value[1].strip()
                    else: # si no se identifico un atributo, entonces tratar de identificar el nombre del bloque
                        blockname = re_blockname.findall(line)
                        if blockname:
                            current_blockname = blockname[0].strip('[]')
    except Exception as inst:
        print(f"{inst}")
        return None
    return cfg