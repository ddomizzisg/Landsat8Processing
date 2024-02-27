import json
import os
import sys
import database.db_connector
from data import data
from datetime import date

def storeValues(name,description,containers,td_schema):
	#print(td_schema)
	database.db_connector.insert_app(name,description,containers,td_schema)

def generateTDSchema(name,description,actions,containers,root):
	workspace = "http://www.adaptivez.org.mx/model/WoTmodel"
	ontology = workspace+"/DockerFUOntology"
	today = str(date.today())
	id_global = workspace+"/applications/app_"+name
	td_schema = {
	    "@context": [
	    	"https://www.w3.org/2019/wot/td/v1",
	    	{	"@language": "en",
	            "dockont": ontology
	        }
	    ],
	    "version": "1.0.0",
	    "created": today,
	    "id": id_global,
	    "title": name,
	    "@type": "dockont:MultiContainerApplication",
	    "description": description
	}

	act = getActions(actions,id_global)
	if (len(act) > 0) :
		td_schema["actions"] = act
	
	prop = getProperties(containers,workspace,root)
	td_schema["properties"] = prop
	print("The container representation has been generated")

	return td_schema


def getActions(actions,id_global):
	act = {}
	descriptions_list = []
	actions_list = []
	inputs_list = []
	outputs_list =[]

	if not actions:
		print("No actions for the app")
	else:
		for i in range(0,len(actions)):
			for j in range(0,len(actions[i])):
				if(type(actions[i][j]) != list):
					act[actions[i][j]] = {"description":"","input":{},"output":{},"forms":[{}]}
					actions_list.append(actions[i][j])
					descriptions_list.append(actions[i][j+1][1])
				else:
					if(actions[i][j][0] == "input"):
						inputs_list.append(i)
						inputs_list.append(actions[i][j][1])
						inputs_list.append(actions[i][j][2])
					else:
						if(actions[i][j][0] == "output"):
							outputs_list.append(i)
							outputs_list.append(actions[i][j][1])
							outputs_list.append(actions[i][j][2])
		for i in range(0,len(act)):
			act[actions_list[i]]["description"] = descriptions_list[i]
			if(len(inputs_list) != 0):
				act[actions_list[i]]["input"] = {"type":"object","properties":{}}
				for j in range(0,len(inputs_list)):
					if(inputs_list[j] == i):
						act[actions_list[i]]["input"]["properties"][inputs_list[j+1]]={"type":inputs_list[j+2]}
			if(len(outputs_list) != 0):
				act[actions_list[i]]["output"] = {"type":"object","properties":{}}
				for j in range(0,len(outputs_list)):
					if(outputs_list[j] == i):
						act[actions_list[i]]["output"]["properties"][outputs_list[j+1]]={"type":outputs_list[j+2]}
			act[actions_list[i]]["forms"] = [{"href":id_global+"/"+actions_list[i]}]
	return act


def getProperties(containers,workspace,root):
	prop = {}
	if not containers:
		print("No containers for the app")
	else:
		for i in range(0,len(containers)):
			content = database.db_connector.select_container_tdSchema(containers[i])
			#file = containers[i]+".json"
			#if os.path.exists(root+"/json_files/containers/"+file):
			#	f = open(root+"/json_files/containers/"+file, "r")
			#	content = f.read()
			#content = content.split("\n")
			#print(content)
			content = content.replace("'", '"') 
			j_content = json.loads(content)
			prop[j_content["title"]] = {"@type":"dockont:Container","description":j_content["description"],"forms":[{"href":workspace+"/container_"+containers[i]}]}

	return prop


def getDataFile(file,name,root):
	array = []
	containers = []
	description = ""
	if os.path.exists(root+"/info_files/applications/"+file):
		f = open(root+"/info_files/applications/"+file, "r")
		content = f.read()
		content = content.split("\n")
		actions = []
		descriptions = []
		inputs = []
		outputs = []
		description = content[0]
		for i in range(1,len(content)):
			if(content[i] == "cont"):
				containers.append(content[i+1])
			if(content[i] == "act"):
				inputs = []
				outputs = []
				actions.append(content[i+1])
				descriptions.append("description")
				descriptions.append(content[i+2])
				actions.append(descriptions)
			if(content[i] == "input"):
				inputs.append("input")
				inputs.append(content[i+1])
				inputs.append(content[i+2])
				actions.append(inputs)
				inputs = []
			if(content[i] == "output"):
				outputs.append("output")
				outputs.append(content[i+1])
				outputs.append(content[i+2])
				actions.append(outputs)
				outputs = []
				if(i+2 == len(content)-1):
					array.append(actions)
				else:
					array.append(actions)
					actions = []
					descriptions = []
	else:
		print("No app information with name: "+name)
	return array,containers,description

def getInfo():
	array = []
	acts = []
	inps = []
	outs = []
	conts = []
	string2 = ""
	name = input("\nApp name (Please verify that it is the same name as the YML file.): ")
	string2 = string2 + "App " + name + "\n"
	description = input("App description: ")
	string2 = string2 + description + "\n"
	cont = "y"
	sum0 = 0
	while(cont == "y"):
		print("\nif you want to add a CONTAINER press \"y\" otherwise press \"n\"")
		cont = input("")
		if(cont == "y"):
			sum0 = sum0 + 1
			string2 = string2 + "\tContainer "+str(sum0)+": \n"
			id_container = input("ID Container: ")
			conts.append(id_container)
			string2 = string2 + "\t" + id_container + "\n"
		else:
			sum0 = 0
			break
	act = "y"
	sum1 = 0
	sum2 = 0
	sum3 = 0
	while(act == "y"):
		print("\nif you want to add an ACTION press \"y\" otherwise press \"n\"")
		act = input("")
		if(act == "y"):
			sum1 = sum1 + 1
			string2 = string2 + "\tAction "+str(sum1)+": \n"
			act_name = input("Action name: ")
			act_desc = input("Action description: ")
			act_name = act_name.lower()
			acts.append(act_name)
			acts.append(act_desc)
			string2 = string2 + "\t" + act_name + "\n"
			string2 = string2 + "\t" + act_desc + "\n"
			inp = "y"
			while(inp == "y"):
				print("\nif you want to add an INPUT for the ACTION press \"y\" otherwise press \"n\"")
				inp = input("")
				if(inp == "y"):
					sum2 = sum2 + 1
					string2 = string2 + "\t\tInput "+str(sum2)+": \n"
					inp_name = input("Input name: ")
					inp_type = input("Input type: ")
					inp_name = inp_name.lower()
					inp_type = inp_type.lower()
					string2 = string2 + "\t \t" + inp_name + "\n"
					string2 = string2 + "\t \t" + inp_type + "\n"
					inps.append(inp_name)
					inps.append(inp_type)
					acts.append(inps)
				else:
					sum2 = 0
					break
			out = "y"
			while(out == "y"):
				print("\nif you want to add an OUTPUT for the ACTION press \"y\" otherwise press \"n\"")
				out = input("")
				if(out == "y"):
					sum3 = sum3 + 1
					string2 = string2 + "\t\tOutput "+str(sum3)+":\n"
					out_name = input("Input name: ")
					out_type = input("Input type: ")
					out_name = out_name.lower()
					out_type = out_type.lower()
					string2 = string2 + "\t \t" + out_name + "\n"
					string2 = string2 + "\t \t" + out_type + "\n"
					outs.append(out_name)
					outs.append(out_type)
					acts.append(outs)
				else:
					sum3 = 0
					break
			array.append(acts)
			acts = []
		else:
			if(act == "n"):
				break
			else:
				print("Invalid value")

	print(string2)
	print("\nIf everything is ok press \"y\" otherwise press \"n\":")
	r = input("")
	if(r == "y"):
		print("The app information document has already been generated")
		return name,description,conts,array
	else:
		print("Please re-provide the app information")
		return ""


name,description,containers,actions = getInfo()

root = data["root_system"]
file = name.lower()+".cfg"
#actions,containers,description = getDataFile(file,name,root)
if not containers:
	print("Please check the application information or generate the information file again")
else:
	td_schema = generateTDSchema(name,description,actions,containers,root)
	storeValues(name,description,containers,td_schema)
	
