import preprocessing
import compliance
import workflow_discovery
import sys
import os

def main(cfg_path, json_path, yml_path, output_path):
    #preprocesing files
    cfg = preprocessing.read_cfg_file(cfg_path)
    js = preprocessing.read_json_file(json_path)
    yml = preprocessing.read_yml_file(yml_path)

    #compliance
    compliance.compliance(cfg, js, yml, output_path)

    #discover workflow
    workflow = workflow_discovery.discover_workflow(cfg)
    #workflow_discovery.draw_workflow(workflow, output_path)

"""
 Cada directorio dentro de _input_path es reconocido como un sistema de eSalud (debe contener los archivos .cfg, .json y .yml ).
    por cada directorio dentro de _input_path el programa verifica el cumplimiento de las normas nacionales e internacionales y genera los reportes correspondientes en el directorio _output_path
"""
#if len(sys.argv) != 3:
#	print("Please enter all parameters: main.py _input_path _output_path")
#	exit()
#input_path = sys.argv[1].replace("/", "")


cfg_path = sys.argv[1]
json_path = sys.argv[2]
yml_path = sys.argv[3]
output_path = sys.argv[4]

print(json_path)

#search for config files
#dirs = os.listdir(input_path)

main(cfg_path, json_path, yml_path, f"{output_path}")

"""for dir in dirs: #a dir represents a folder that contains config files: .cfg, .json .yml
    cfg_path = ""
    json_path = ""
    yml_path = ""
    files_name = os.listdir(f"{input_path}/{dir}")
    for file in files_name:
        file_name_lower_case = file.lower()
        if ".cfg" in file_name_lower_case:
            cfg_path = f"{input_path}/{dir}/{file}"
        elif ".json" in file_name_lower_case:
            json_path = f"{input_path}/{dir}/{file}"
        elif ".yml" in file_name_lower_case:
            yml_path = f"{input_path}/{dir}/{file}"
    if not os.path.exists(f"{output_path}/{dir}"):
        os.makedirs(f"{output_path}/{dir}")
    main(cfg_path, json_path, yml_path, f"{output_path}/{dir}")"""