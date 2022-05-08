import os
import ntpath
import sys


base = """
    {                                                                                                                                                                                           
        "define" : {                                                                                                                                                                            
            "RANGE" : range(0,%d),                                                                                                                                                               
            "FILELIST" : [ %s ],        
            "NAMEFILES" : [ %s ],
            "MONGOIP" : "148.247.201.224"
        },                                                                                                                                                                                      
        "rules" : [
            {
                "command": "mkdir -p /outputs/"+NAMEFILES[N]+" && tar -xzvf '"+FILELIST[N]+"' -C /outputs/"+NAMEFILES[N] + "> uncompress"+N+".txt",
                "outputs": ["uncompress"+N+".txt"]
            } for N in RANGE,
            {
                "command": "docker exec correcciones python /app/LS.py /outputs/" + NAMEFILES[N] + " " + NAMEFILES[N] + " > corrections"+N+".txt",
                "outputs":  ["corrections"+N+".txt"],
                "inputs":  ["uncompress"+N+".txt"]
            } for N in RANGE,
            {
                "command": "docker exec parser python /app/test.py /outputs/" + NAMEFILES[N] + "/" + NAMEFILES[N] + "_MTL.txt " + NAMEFILES[N] + " " + MONGOIP + " > parser"+N+".txt",
                "outputs":  ["parser"+N+".txt"],
                "inputs":  ["corrections"+N+".txt"]
            } for N in RANGE,
        ]
    }
"""

path_files = sys.argv[1]

files = ["\"%s\"" % os.path.join(dp, f) for dp, dn, filenames in os.walk(path_files) for f in filenames]
files_names = ["\"%s\"" % f.replace(".tar.gz", "") for dp, dn, filenames in os.walk(path_files) for f in filenames]

list_files = ','.join(files)
list_files_names = ','.join(files_names)

define_base = base % (len(files), list_files, list_files_names)


print(define_base) 
