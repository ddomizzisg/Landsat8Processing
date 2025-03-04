import parsl
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import LocalProvider
from parsl.channels import LocalChannel
from parsl.app.app import bash_app
from parsl.data_provider.files import File
import time
import glob
import os
from pathlib import Path

@bash_app
def uncompress(inputs=[], outputs=[]):
    return "mkdir -p %s && tar -xzvf %s -C %s" % (outputs[0], inputs[0], outputs[0])

@bash_app
def derivatives(inputs=[], outputs=[]):
    return "python3 apps/derivatives/LS.py %s %s" % (inputs[0], inputs[1])

@bash_app
def indexing(inputs=[], outputs=[]):
    return "python3 apps/parser/test.py %s %s mongo > %s" % (inputs[0], inputs[1], outputs[0])

@bash_app
def ciphering(inputs=[], outputs=[]):
    return "/apps/aes/CifradorAES %s %s" % (inputs[0], outputs[0])

@bash_app
def ida(inputs=[], outputs=[]):
    return "/apps/ida/CodificationIDA %s %s %s %s %s %s" % (inputs[0], outputs[0], outputs[1], outputs[2], outputs[3], outputs[4])

start_time = time.time()

local_htex = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_Local",
            worker_debug=True,
            cores_per_worker=3,
            max_workers=24,
            provider=LocalProvider(
                channel=LocalChannel(),
                init_blocks=1,
                max_blocks=1,
            ),
        )
    ],
    strategy=None,
)

parsl.clear()
parsl.load(local_htex)

datadir = "/DATA/"

input_data = []
output_uncompress =  []
input_indexing =  []
output_indexing = []
names = []

for filename in glob.iglob(datadir + '**/*.tar.gz', recursive=True):
    input_data.append(File(filename))
    basename = os.path.splitext(os.path.basename(filename))[0].replace(".tar","")
    #output_simulation.append(File("simulation/" + basename + ".csv"))
    output_uncompress.append(File("uncompressed/" + basename))
    input_indexing.append(File("uncompressed/" + basename + "/" + basename + "_MTL.txt"))
    output_indexing.append(File("indexing/" + basename + ".json" ))
    names.append(basename)
    
    

Path("uncompressed").mkdir(parents=True, exist_ok=True)
Path("indexing").mkdir(parents=True, exist_ok=True)

start_time_simulator = time.time()
results = []

# for i in range(len(input_data)):
#     results.append(simulation(inputs=[input_data[i]], outputs=[output_simulation[i]]))

# for r in results:
#     r.result()



uncompress_starttime = time.time()
results = []
for i in range(len(input_data)):
    #print("mkdir -p %s && tar -xzvf %s -C %s" % (output_uncompress[i], input_data[i], output_uncompress[i]))
    results.append(uncompress(inputs=[input_data[i]], outputs=[output_uncompress[i]]))

for r in results:
    r.result()

print("---Uncompress %s seconds ---" % (time.time() - uncompress_starttime))

derivatives_starttime = time.time()

results = []
for i in range(len(input_data)):
    #print("python3 apps/derivatives/LS.py %s %s" % (output_uncompress[i], names[i]))
    results.append(derivatives(inputs=[output_uncompress[i], names[i]], outputs=[]))


for r in results:
    r.result()

print("---Derivatives %s seconds ---" % (time.time() - derivatives_starttime))

indexing_starttime = time.time()
results = []
for i in range(len(input_data)):
    #print("python3 /app/test.py %s %s mongo > %s.json" % (input_indexing[i], names[i], output_indexing[i]))
    results.append(indexing(inputs=[input_indexing[i], names[i]], outputs=[output_indexing[i]]))

for r in results:
     r.result()

print("---Indexing %s seconds ---" % (time.time() - indexing_starttime))

