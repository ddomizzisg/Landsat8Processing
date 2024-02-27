import json
import os
import sys
import datetime
import database.db_connector
from data import data
from datetime import date

def storeValues(id_container,id_long,name,status,volumes,platform,image,description,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p,utility_p,root):
	f = open('representation/tdschemes_private/'+id_container+'.json', "w")
	f.write(td_schema_priv)
	f.close()
	td_schema_pub = str(td_schema_pub)
	td_schema_priv = str(td_schema_priv)
	if(image_p == "y"):
		image_p = 1
	else:
		image_p = 0
	if(volumes_p == "y"):
		volumes_p = 1
	else:
		volumes_p = 0
	if(status_p == "y"):
		status_p = 1
	else:
		status_p = 0
	if(utility_p == "y"):
		utility_p = 1
	else:
		utility_p = 0
	datatime = str(datetime.datetime.now())
	datatime = datatime.split(".")
	database.db_connector.insert_containers(id_container,id_long,name,status,image,volumes,platform,description,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p)
	database.db_connector.insert_containers_utility(id_container,id_long,0,0,0,0,0,0,0,0,datatime[0],utility_p)
	

def generateTDSchema(id_container,name,description,actions,root,id_long,status_p,image_p,volumes_p,utility_p,actions_p):
	workspace = "http://www.adaptivez.org.mx/WoTmodel"
	ontology = workspace+"/DockerFUOntology"
	today = str(date.today())
	id_global = workspace+"/containers/container_"+id_container
	id_priv = workspace+"/containers/container_"+id_long
	td_schema_pub = {
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
		"@type": "dockont:Container",
		"description": description,
		"properties": {
			"id": {
			"@type": "dockont:id",
			"type": "string",
			"description": "Container local ID provided by the docker daemon",
			"forms": [{"href": id_global+"/id"}]
			},
			"name": {
				"@type": "dockont:name",
				"type": "string",
				"description": "Container name provided by creator",
				"forms": [{"href": id_global+"/name"}]
			},
			"platform": {
				"@type": "dockont:platform",
				"type": "string",
				"description": "Platform with which the container was created (e.g. Docker)",
				"forms": [{"href": id_global+"/platform"}]
			},
			"status": {
				"@type": "dockont:status",
				"type": "string",
				"description": "Container status (e.g. created, restarting, running, removing, paused, exited, dead)",
				"forms": [{"href": "private"}]
			},
			"cpu_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container CPU utilization",
				"forms": [{"href": "private"}]
			},
			"memory_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container memory utilization",
				"forms": [{"href": "private"}]
			},
			"network_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container network utilization",
				"forms": [{"href": "private"}]
			},
			"fileSystem_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container file system utilization",
				"forms": [{"href": "private"}]
			},
			"image": {
				"@type": "dockont:id",
				"type": "string",
				"description": "Image ID with which the container was created",
				"forms": [{"href": "private"}]
			},
			"volumes": {
				"@type": "dockont:volumes",
				"type": "boolean",
				"description": "Boolean value to know if the container has any volume",
				"forms": [{"href": "private"}]
			},
		},
		"events": {
			"cpu_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"cpu_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"cpu_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"memory_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"memory_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"memory_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"network_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"network_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"network_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"fileSystem_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"fileSystem_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"fileSystem_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			}

		}
	}

	td_schema_priv = {
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
		"@type": "dockont:Container",
		"description": description,
		"properties": {
			"id": {
			"@type": "dockont:id",
			"type": "string",
			"description": "Container local ID provided by the docker daemon",
			"forms": [{"href": id_global+"/id"}]
			},
			"name": {
				"@type": "dockont:name",
				"type": "string",
				"description": "Container name provided by creator",
				"forms": [{"href": id_global+"/name"}]
			},
			"platform": {
				"@type": "dockont:platform",
				"type": "string",
				"description": "Platform with which the container was created (e.g. Docker)",
				"forms": [{"href": id_global+"/platform"}]
			},
			"status": {
				"@type": "dockont:status",
				"type": "string",
				"description": "Container status (e.g. created, restarting, running, removing, paused, exited, dead)",
				"forms": [{"href": "private"}]
			},
			"cpu_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container CPU utilization",
				"forms": [{"href": "private"}]
			},
			"memory_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container memory utilization",
				"forms": [{"href": "private"}]
			},
			"network_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container network utilization",
				"forms": [{"href": "private"}]
			},
			"fileSystem_utilization": {
				"@type": "dockont:utilization",
				"type": "number",
				"description": "Container file system utilization",
				"forms": [{"href": "private"}]
			},
			"image": {
				"@type": "dockont:id",
				"type": "string",
				"description": "Image ID with which the container was created",
				"forms": [{"href": "private"}]
			},
			"volumes": {
				"@type": "dockont:volumes",
				"type": "boolean",
				"description": "Boolean value to know if the container has any volume",
				"forms": [{"href": "private"}]
			},
		},
		"events": {
			"cpu_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"cpu_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"cpu_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"memory_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"memory_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"memory_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"network_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"network_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"network_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"fileSystem_utilization_high":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"fileSystem_utilization_medium":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			},
			"fileSystem_utilization_low":{
				"data": {
					"@type":"dockont:utilizationLevel",
					"type": "boolean"},
				"forms": [{
					"href": "private"
				}]
			}

		}
	}
	td_schema_pub = generateTDSchemaPub(id_global,id_priv,actions,status_p,image_p,volumes_p,utility_p,actions_p,td_schema_pub)
	
	td_schema_priv = generateTDSchemaPriv(id_global,id_priv,actions,status_p,image_p,volumes_p,utility_p,actions_p,td_schema_priv)
	return td_schema_pub,td_schema_priv

def generateTDSchemaPub(id_global,id_priv,actions,status_p,image_p,volumes_p,utility_p,actions_p,td_schema):
	td_schema_pub = td_schema
	if(status_p == "y"):
		td_schema_pub["properties"]["status"]["forms"] = [{"href":id_global+"/status"}] 
	if(image_p == "y"):
		td_schema_pub["properties"]["image"]["forms"] = [{"href":id_global+"/image"}] 
	if(volumes_p == "y"):
		td_schema_pub["properties"]["volumes"]["forms"] = [{"href":id_global+"/volumes"}] 
	if(utility_p == "y"):
		td_schema_pub["properties"]["cpu_utilization"]["forms"] = [{"href":id_global+"/cpu_util"}] 
		td_schema_pub["properties"]["memory_utilization"]["forms"] = [{"href":id_global+"/mem_util"}]
		td_schema_pub["properties"]["network_utilization"]["forms"] = [{"href":id_global+"/net_util"}]
		td_schema_pub["properties"]["fileSystem_utilization"]["forms"] = [{"href":id_global+"/fs_util"}]
		td_schema_pub["events"]["cpu_utilization_high"]["forms"] = [{"href":id_global+"/cpu_util_high"}]
		td_schema_pub["events"]["cpu_utilization_medium"]["forms"] = [{"href":id_global+"/cpu_util_medium"}]
		td_schema_pub["events"]["cpu_utilization_low"]["forms"] = [{"href":id_global+"/cpu_util_low"}]
		td_schema_pub["events"]["memory_utilization_high"]["forms"] = [{"href":id_global+"/mem_util_high"}]
		td_schema_pub["events"]["memory_utilization_medium"]["forms"] = [{"href":id_global+"/mem_util_medium"}]
		td_schema_pub["events"]["memory_utilization_low"]["forms"] = [{"href":id_global+"/mem_util_low"}]
		td_schema_pub["events"]["network_utilization_high"]["forms"] = [{"href":id_global+"/net_util_high"}]
		td_schema_pub["events"]["network_utilization_medium"]["forms"] = [{"href":id_global+"/net_util_medium"}]
		td_schema_pub["events"]["network_utilization_low"]["forms"] = [{"href":id_global+"/net_util_low"}]
		td_schema_pub["events"]["fileSystem_utilization_high"]["forms"] = [{"href":id_global+"/fs_util_high"}]
		td_schema_pub["events"]["fileSystem_utilization_medium"]["forms"] = [{"href":id_global+"/fs_util_medium"}]
		td_schema_pub["events"]["fileSystem_utilization_low"]["forms"] = [{"href":id_global+"/fs_util_low"}]
	if not actions:
		print("\nNo actions for container")
	else:
		act = getActions(actions,id_global,actions_p,"public",id_priv)
		td_schema_pub["actions"] = act
	#print(td_schema)
	print("\nThe public container representation has been generated \n")
	return td_schema_pub

def generateTDSchemaPriv(id_global,id_priv,actions,status_p,image_p,volumes_p,utility_p,actions_p,td_schema):
	td_schema_priv = td_schema
	td_schema_priv["properties"]["status"]["forms"] = [{"href":id_priv+"/status"}]
	td_schema_priv["properties"]["image"]["forms"] = [{"href":id_priv+"/image"}]
	td_schema_priv["properties"]["volumes"]["forms"] = [{"href":id_priv+"/volumes"}]
	td_schema_priv["properties"]["cpu_utilization"]["forms"] = [{"href":id_priv+"/cpu_util"}] 
	td_schema_priv["properties"]["memory_utilization"]["forms"] = [{"href":id_priv+"/mem_util"}]
	td_schema_priv["properties"]["network_utilization"]["forms"] = [{"href":id_priv+"/net_util"}]
	td_schema_priv["properties"]["fileSystem_utilization"]["forms"] = [{"href":id_priv+"/fs_util"}]
	td_schema_priv["events"]["cpu_utilization_high"]["forms"] = [{"href":id_priv+"/cpu_util_high"}]
	td_schema_priv["events"]["cpu_utilization_medium"]["forms"] = [{"href":id_priv+"/cpu_util_medium"}]
	td_schema_priv["events"]["cpu_utilization_low"]["forms"] = [{"href":id_priv+"/cpu_util_low"}]
	td_schema_priv["events"]["memory_utilization_high"]["forms"] = [{"href":id_priv+"/mem_util_high"}]
	td_schema_priv["events"]["memory_utilization_medium"]["forms"] = [{"href":id_priv+"/mem_util_medium"}]
	td_schema_priv["events"]["memory_utilization_low"]["forms"] = [{"href":id_priv+"/mem_util_low"}]
	td_schema_priv["events"]["network_utilization_high"]["forms"] = [{"href":id_priv+"/net_util_high"}]
	td_schema_priv["events"]["network_utilization_medium"]["forms"] = [{"href":id_priv+"/net_util_medium"}]
	td_schema_priv["events"]["network_utilization_low"]["forms"] = [{"href":id_priv+"/net_util_low"}]
	td_schema_priv["events"]["fileSystem_utilization_high"]["forms"] = [{"href":id_priv+"/fs_util_high"}]
	td_schema_priv["events"]["fileSystem_utilization_medium"]["forms"] = [{"href":id_priv+"/fs_util_medium"}]
	td_schema_priv["events"]["fileSystem_utilization_low"]["forms"] = [{"href":id_priv+"/fs_util_low"}]
	if not actions:
		print("\nNo actions for container")
	else:
		act = getActions(actions,id_global,actions_p,"private",id_priv)
		td_schema_priv["actions"] = act
	print("\nThe private container representation has been generated \n")
	return td_schema_priv



def getActions(actions,id_global,actions_p,pp,id_long):
	act = {}
	descriptions_list = []
	actions_list = []
	inputs_list = []
	outputs_list =[]
	for i in range(0,len(actions)):
		for j in range(0,len(actions[i])):
			if(type(actions[i][j]) != list and type(actions[i][j+1]) != list):
				act[actions[i][j]] = {"description":"","input":{},"output":{},"forms":[{}]}
				actions_list.append(actions[i][j])
				descriptions_list.append(actions[i][j+1])
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
		if(pp == "public"):
			if(actions_p[i]=="y"):
				act[actions_list[i]]["forms"] = [{"href":id_global+"/"+actions_list[i]}]
			else:act[actions_list[i]]["forms"] = [{"href":"private"}]
		else:
			act[actions_list[i]]["forms"] = [{"href":id_long+"/"+actions_list[i]}]

	return act


"""def getDataFile(file,id_container,root):
	array = []
	description = ""
	if os.path.exists(root+"/info_files/containers/"+file):
		f = open(root+"/info_files/containers/"+file, "r")
		content = f.read()
		content = content.split("\n")
		description = content[0]
		actions = []
		descriptions = []
		inputs = []
		outputs = []
		for i in range(1,len(content)):
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
	return description,array"""
	

def getDataInspect(id_container):
	res = os.popen("docker inspect "+id_container)
	data = json.loads(res.read())
	id_long = data[0]["Id"]
	name = data[0]["Name"]
	name = name.split("/")
	name = name[1]
	status = data[0]["State"]["Status"]
	mounts = data[0]["Mounts"]
	if not mounts:
		volumes = 0
	else:
		volumes = 1
	platform = "Docker"
	image = data[0]["Config"]["Image"]

	return id_long,name,status,volumes,platform,image

def getInfo():
	array = []
	acts = []
	inps = []
	outs = []
	string2 = ""
	print("\n-------------------------------------------------------------------------------------------------------")
	print("\nPlease provide the container information requested")
	id_container = input("\nContainer ID (Docker): ")
	string2 = string2 + "Container "+id_container+"\n"
	description = input("\nContainer description: ")
	string2 = string2 + description + "\n"
	act = "y"
	sum1 = 0
	sum2 = 0
	sum3 = 0
	while(act == "y"):
		print("\nIf you want to add an ACTION press \"y\" otherwise press \"n\"")
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
				print("\nIf you want to add an INPUT for the ACTION press \"y\" otherwise press \"n\"")
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
					inps.append("input")
					inps.append(inp_name)
					inps.append(inp_type)
					acts.append(inps)
					inps = []
				else:
					sum2 = 0
					break
			out = "y"
			while(out == "y"):
				print("\nIf you want to add an OUTPUT for the ACTION press \"y\" otherwise press \"n\"")
				out = input("")
				if(out == "y"):
					sum3 = sum3 + 1
					string2 = string2 + "\t\tOutput "+str(sum3)+":\n"
					out_name = input("Output name: ")
					out_type = input("Output type: ")
					out_name = out_name.lower()
					out_type = out_type.lower()
					string2 = string2 + "\t \t" + out_name + "\n"
					string2 = string2 + "\t \t" + out_type + "\n"
					outs.append("output")
					outs.append(out_name)
					outs.append(out_type)
					acts.append(outs)
					outs = []
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
		print("The container information has been saved")
		return id_container,description,array
	else:
		print("Please re-provide the container information")
		return ""
	print("\n-------------------------------------------------------------------------------------------------------")

def getInfoP(actions):
	print("\n-------------------------------------------------------------------------------------------------------")
	print('\nPlease press "y" if you want the property public otherwise press "n" if you want the property private')
	status_p = input("\nStatus: ")
	image_p = input("\nImage: ")
	volumes_p = input("\nVolumes: ")
	utility_p = input("\nUtilization Factors (CPU, Memory, Network FileSystem): ")
	actions_p = []
	if(len(actions)>0):
		for i in range(0,len(actions)):
			actions_p.append(input("\nAction '"+actions[i][0]+"': "))
	print("\n-------------------------------------------------------------------------------------------------------")
	return status_p,image_p,volumes_p,utility_p,actions_p

id_container,description,actions = getInfo()
print(actions)
root = data["root_system"]
if not description:
	print("There is no description of the container. Please check the application information or generate the information file again")
else:
	status_p,image_p,volumes_p,utility_p,actions_p = getInfoP(actions)
	id_long,name,status,volumes,platform,image = getDataInspect(id_container)
	td_schema_pub,td_schema_priv = generateTDSchema(id_container,name,description,actions,root,id_long,status_p,image_p,volumes_p,utility_p,actions_p)
	td_schema_pub = str(td_schema_pub)
	td_schema_priv = str(td_schema_priv)
	print(td_schema_pub)
	print("*********************************************************************************************")
	print(td_schema_priv)
	#print("ID LONG: "+str(id_long))
	storeValues(id_container,id_long,name,status,volumes,platform,image,description,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p,utility_p,root)

