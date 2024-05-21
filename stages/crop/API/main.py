
from flask import Flask, request
from flask_api import status
import json
from flask import Response
from flask import jsonify
from flask_api import status
import os
import datetime
import subprocess
import shlex

app = Flask(__name__)
app.debug = True

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/api/ejecuta', methods=['POST'])
def ejecuta():
    content = request.json
    command = content['command']
    parameters = content['data']
    command = command + ' ' + ' '.join(parameters)

    start_time = datetime.datetime.now() #start measuring the execution time
    #result_cmd = subprocess.run(command.split(' '), stdout=subprocess.PIPE) #execute command
    cmd_args = shlex.split(command)
    pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = pipes.communicate()
    end_time = datetime.datetime.now() #end measuring the execution time

    time_diff = (end_time - start_time) #get the response time
    execution_time = time_diff.total_seconds() * 1000 #to miliseconds

    #response json
    result = {
        "stdout":std_out.strip().decode("utf-8"),
        "stderr": std_err.strip().decode("utf-8"),
        "code":str(pipes.returncode),
        "response_time": execution_time
        }
    return jsonify(result), status.HTTP_200_OK

@app.route('/api/call', methods=['POST'])
def call():
    content = request.json
    name = content['service_name']
    data = content['data']
    r = request.post("http://%s:5000/api/ejecuta" % name, json=data)
    results = r.json()
    return results, status.HTTP_200_OK

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
