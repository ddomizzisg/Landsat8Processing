import json
import time
import os

from dagon import Workflow
from dagon.task import DagonTask, TaskType

# Check if this is the main
if __name__ == '__main__':
    # Create the orchestration workflow
    workflow = Workflow("DataFlow-Demo-Server", max_threads=2)

    # Set the dry
    #workflow.set_dry(False)

    imgs_path = "/home/domizzi/Documents/landsat8/"
    MONGO_IP = "192.168.1.79"
    # get the input files
    imgs = [{"path":os.path.join(dp, f), "name":f} for dp, dn, filenames in os.walk(imgs_path) for f in filenames]

    # Uncompress tasks
    aux = 0
    for i in imgs:
        path = i['path']
        name = i['name'].replace(".tar.gz", "")
        taskUncompress = DagonTask(TaskType.BATCH, "uncompress%d" % aux, "tar -xzvf %s" % path)
        taskCorrections = DagonTask(TaskType.DOCKER, "corrections%d" % aux, "python /app/LS.py workflow:///uncompress%d %s" % (aux, name),
                                    image="corrections:landsat")
        taskIndexing = DagonTask(TaskType.DOCKER, "indexing%d" % aux,
                                    "python /app/test.py workflow:///uncompress%d/%s_MTL.txt %s %s > data.json" % (aux, name, name, MONGO_IP),
                                 image="parser:landsat")

        workflow.add_task(taskUncompress)
        #workflow.add_task(taskCorrections)
        workflow.add_task(taskIndexing)
        aux += 1

    workflow.make_dependencies()

    # run the workflow
    workflow.run()
