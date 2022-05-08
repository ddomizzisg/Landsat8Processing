from flask import Flask
from flask import render_template
import ogr
import os
import csv
import json 
from flask import jsonify
import requests
import hashlib
import subprocess


app = Flask(__name__)
app.debug = True

@app.route("/generate/<img>")
def generate(img):
	bashCommand = "python LS.py " + img
	print(bashCommand)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	#output, error = process.communicate()
	#print(output)
	#print(error)
	process.wait()
	#process.terminate()
	return img

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0') 
