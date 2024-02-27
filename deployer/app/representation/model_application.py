import json
import os
import sys
import datetime
import ast
import database.db_connector
import time
from data import data
from datetime import date

def storeValuesApp(app_name,app_description,containers_info,app_td_schema,json_structure,extras, folder):
	containers_id = []
	#print(containers_info)
	for i in range(0,len(containers_info)):
		containers_id.append(containers_info[i][0])
		td_schema_pub = str(containers_info[i][20])
		td_schema_priv = str(containers_info[i][21])
		td_schema_pub = td_schema_pub.replace("'",'"')
		td_schema_priv = td_schema_priv.replace("'",'"')
		
		id_container = containers_info[i][0]
		id_long = containers_info[i][1]
		name = containers_info[i][2]
		description = containers_info[i][3]
		status = containers_info[i][4]
		volumes = containers_info[i][5]
		platform = containers_info[i][6]
		image = containers_info[i][7]
		docker_port = containers_info[i][8]
		host_port = containers_info[i][9]
		entrypoint = containers_info[i][10]
		image_p = containers_info[i][12]
		volumes_p = containers_info[i][13]
		status_p = containers_info[i][11]
		utility_p = containers_info[i][14]

		storeValuesConts(id_container,id_long,name,status,volumes,platform,image,description,docker_port,host_port,entrypoint,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p,utility_p,extras)
		if(containers_info[i][19]):
			for j in range(0,len(containers_info[i][19])):
				storeValuesActs(containers_info[i][19][j][0],containers_info[i][19][j][2],containers_info[i][0])
	app_td_schema = str(app_td_schema)
	app_td_schema = app_td_schema.replace("'",'"')
	print("HOLA", app_name, app_description)
	database.db_connector.insert_app(app_name,app_description,containers_id,app_td_schema)
	f = open(folder + app_name+"_td_app.txt", "a")
	f.write(app_td_schema)
	f.close()
	json_structure = str(json_structure)
	json_structure = json_structure.replace("'",'"')
	database.db_connector.insert_app_structure(app_name,json_structure,".")

def storeValuesConts(id_container,id_long,name,status,volumes,platform,image,description,docker_port,host_port,entrypoint,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p,utility_p,extras):
	f = open('representation/tdschemes_private/'+id_container+'.json', "w")
	f.write(td_schema_priv)
	f.close()
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
	
	#print(id_container,id_long,name,status,image,volumes,entrypoint,platform,description,docker_port,host_port,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p)

	database.db_connector.insert_containers(id_container,id_long,name,status,image,volumes,entrypoint,platform,description,docker_port,host_port,td_schema_pub,td_schema_priv,image_p,volumes_p,status_p)
	database.db_connector.insert_containers_utility(id_container,id_long,0,0,0,0,0,0,0,0,datatime[0],utility_p)
	f = open(name+"_td.txt", "a")
	f.write(td_schema_pub)
	f.close()
	for i in range(0,len(extras)):
		if(extras[i][0] == name):
			database.db_connector.insert_containers_extras(extras[i][0],extras[i][1],extras[i][2],extras[i][3])

def storeValuesActs(name_action,uri,id_container):
	database.db_connector.insert_actions(name_action,uri,id_container)

def generateTDSchemaApp(name,description,containers):
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
	    "description": description,
		"properties":{
		}

	}
	prop = getPropertiesApp(containers,workspace)
	td_schema["properties"]["containers"] = prop
	td_schema["properties"]["edges"] = {"@type": "dockont:edges","type": "string","description": "Edges between the containers that make up the multi-container application (e.g. Container 1 send to Container 2, Container 3 receives from Container 2)","forms": [{"href":  id_global+"/edges"}]}
	return td_schema

def generateTDSchemasConts(app,containers_info):
	#print("***********************************************************")
	#print(containers_info)
	for i in range(0,len(containers_info)):
		td_schema_pub,td_schema_priv = generateTDSchemaCont(app,containers_info[i][0],containers_info[i][2],containers_info[i][3],containers_info[i][19],containers_info[i][1],containers_info[i][11],containers_info[i][12],containers_info[i][13],containers_info[i][14],containers_info[i][15],containers_info[i][16],containers_info[i][17],containers_info[i][18])
		containers_info[i].append(td_schema_pub)
		containers_info[i].append(td_schema_priv)
	return containers_info

def generateTDSchemaCont(app,id_container,name,description,actions,id_long,status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p):
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
			"general": {
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
				"entrypoint": {
					"@type": "dockont:entrypoint",
					"type": "boolean",
					"description": "Script list (separated by comma)to know what application is executing the container and the arguments",
					"forms": [{"href": "private"}]
				}
			},
			"behavior": {
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
				}
			},
			"structure": {
				"send_to":{
					"@type": "dockont:structure",
					"type": "array",
					"description": "Containers to which it send information",
					"forms": [{"href": "private"}]
				},
				"receives_from":{
					"@type": "dockont:structure",
					"type": "array",
					"description": "Containers from which it receives information",
					"forms": [{"href": "private"}]
				}
			},
		},
		"events": {
			"behavior":{
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
			},
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
			"general": {
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
				"entrypoint": {
					"@type": "dockont:entrypoint",
					"type": "boolean",
					"description": "Script list (separated by comma)to know what application is executing the container and the arguments",
					"forms": [{"href": "private"}]
				}
			},
			"behavior": {
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
				}
			},
			"structure": {
				"send_to":{
					"@type": "dockont:structure",
					"type": "array",
					"description": "Containers to which it send information",
					"forms": [{"href": "private"}]
				},
				"receives_from":{
					"@type": "dockont:structure",
					"type": "array",
					"description": "Containers from which it receives information",
					"forms": [{"href": "private"}]
				}
			}
		},
		"events": {
			"behavior":{
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
	}

	td_schema_pub,extras,extras_e = getExtraTDSchema(td_schema_pub,app,name)
	td_schema_priv,extras,extras_e = getExtraTDSchema(td_schema_priv,app,name)

	extras = list(extras)
	extras_e = list(extras_e)


	td_schema_pub = generateTDSchemaPub(id_global,id_priv,actions,extras,extras_e,status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p,td_schema_pub)
	td_schema_priv = generateTDSchemaPriv(id_global,id_priv,actions,extras,extras_e,actions_p,td_schema_priv)
	
	
	return td_schema_pub,td_schema_priv

def generateTDSchemaPub(id_global,id_priv,actions,extras,extras_e,status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p,td_schema):
	td_schema_pub = td_schema
	if(status_p == "y"):
		td_schema_pub["properties"]["general"]["status"]["forms"] = [{"href":id_global+"/status"}] 
		#se toma que cuando el status sea pub el entrypoint tmb
		td_schema_pub["properties"]["general"]["entrypoint"]["forms"] = [{"href":id_global+"/entrypoint"}] 

	if(image_p == "y"):
		td_schema_pub["properties"]["general"]["image"]["forms"] = [{"href":id_global+"/image"}] 
	if(volumes_p == "y"):
		td_schema_pub["properties"]["general"]["volumes"]["forms"] = [{"href":id_global+"/volumes"}] 
	if(structure_p == "y"):
		td_schema_pub["properties"]["structure"]["send_to"]["forms"] = [{"href":id_global+"/sendto"}] 
		td_schema_pub["properties"]["structure"]["receives_from"]["forms"] = [{"href":id_global+"/receivesfrom"}] 
	if(utility_p == "y"):
		td_schema_pub["properties"]["behavior"]["cpu_utilization"]["forms"] = [{"href":id_global+"/cpu_util"}] 
		td_schema_pub["properties"]["behavior"]["memory_utilization"]["forms"] = [{"href":id_global+"/mem_util"}]
		td_schema_pub["properties"]["behavior"]["network_utilization"]["forms"] = [{"href":id_global+"/net_util"}]
		td_schema_pub["properties"]["behavior"]["fileSystem_utilization"]["forms"] = [{"href":id_global+"/fs_util"}]
		td_schema_pub["events"]["behavior"]["cpu_utilization_high"]["forms"] = [{"href":id_global+"/cpu_util_high"}]
		td_schema_pub["events"]["behavior"]["cpu_utilization_medium"]["forms"] = [{"href":id_global+"/cpu_util_medium"}]
		td_schema_pub["events"]["behavior"]["cpu_utilization_low"]["forms"] = [{"href":id_global+"/cpu_util_low"}]
		td_schema_pub["events"]["behavior"]["memory_utilization_high"]["forms"] = [{"href":id_global+"/mem_util_high"}]
		td_schema_pub["events"]["behavior"]["memory_utilization_medium"]["forms"] = [{"href":id_global+"/mem_util_medium"}]
		td_schema_pub["events"]["behavior"]["memory_utilization_low"]["forms"] = [{"href":id_global+"/mem_util_low"}]
		td_schema_pub["events"]["behavior"]["network_utilization_high"]["forms"] = [{"href":id_global+"/net_util_high"}]
		td_schema_pub["events"]["behavior"]["network_utilization_medium"]["forms"] = [{"href":id_global+"/net_util_medium"}]
		td_schema_pub["events"]["behavior"]["network_utilization_low"]["forms"] = [{"href":id_global+"/net_util_low"}]
		td_schema_pub["events"]["behavior"]["fileSystem_utilization_high"]["forms"] = [{"href":id_global+"/fs_util_high"}]
		td_schema_pub["events"]["behavior"]["fileSystem_utilization_medium"]["forms"] = [{"href":id_global+"/fs_util_medium"}]
		td_schema_pub["events"]["behavior"]["fileSystem_utilization_low"]["forms"] = [{"href":id_global+"/fs_util_low"}]
	if(extras_p == "y"):
		for i in range(0,len(extras)):
			td_schema_pub["properties"]["extra"][extras[i]]["forms"] = [{"href":id_global+"/extras/"+str(extras[i])}] 
	if(extras_ep == "y"):
		for i in range(0,len(extras_e)):
			td_schema_pub["events"]["extra"][extras_e[i]]["forms"] = [{"href":id_global+"/extras/"+str(extras_e[i])}] 
	if actions:
		act = getActions(actions,id_global,actions_p,"public",id_priv)
		td_schema_pub["actions"] = act
	return td_schema_pub

def generateTDSchemaPriv(id_global,id_priv,actions,extras,extras_e,actions_p,td_schema):
	td_schema_priv = td_schema
	td_schema_priv["properties"]["general"]["status"]["forms"] = [{"href":id_priv+"/status"}]
	td_schema_priv["properties"]["structure"]["send_to"]["forms"] = [{"href":id_priv+"/sendto"}]
	td_schema_priv["properties"]["structure"]["receives_from"]["forms"] = [{"href":id_priv+"/receivesfrom"}]
	td_schema_priv["properties"]["general"]["image"]["forms"] = [{"href":id_priv+"/image"}]
	td_schema_priv["properties"]["general"]["volumes"]["forms"] = [{"href":id_priv+"/volumes"}]
	td_schema_priv["properties"]["general"]["entrypoint"]["forms"] = [{"href":id_priv+"/entrypoint"}]
	td_schema_priv["properties"]["behavior"]["cpu_utilization"]["forms"] = [{"href":id_priv+"/cpu_util"}] 
	td_schema_priv["properties"]["behavior"]["memory_utilization"]["forms"] = [{"href":id_priv+"/mem_util"}]
	td_schema_priv["properties"]["behavior"]["network_utilization"]["forms"] = [{"href":id_priv+"/net_util"}]
	td_schema_priv["properties"]["behavior"]["fileSystem_utilization"]["forms"] = [{"href":id_priv+"/fs_util"}]
	td_schema_priv["events"]["behavior"]["cpu_utilization_high"]["forms"] = [{"href":id_priv+"/cpu_util_high"}]
	td_schema_priv["events"]["behavior"]["cpu_utilization_medium"]["forms"] = [{"href":id_priv+"/cpu_util_medium"}]
	td_schema_priv["events"]["behavior"]["cpu_utilization_low"]["forms"] = [{"href":id_priv+"/cpu_util_low"}]
	td_schema_priv["events"]["behavior"]["memory_utilization_high"]["forms"] = [{"href":id_priv+"/mem_util_high"}]
	td_schema_priv["events"]["behavior"]["memory_utilization_medium"]["forms"] = [{"href":id_priv+"/mem_util_medium"}]
	td_schema_priv["events"]["behavior"]["memory_utilization_low"]["forms"] = [{"href":id_priv+"/mem_util_low"}]
	td_schema_priv["events"]["behavior"]["network_utilization_high"]["forms"] = [{"href":id_priv+"/net_util_high"}]
	td_schema_priv["events"]["behavior"]["network_utilization_medium"]["forms"] = [{"href":id_priv+"/net_util_medium"}]
	td_schema_priv["events"]["behavior"]["network_utilization_low"]["forms"] = [{"href":id_priv+"/net_util_low"}]
	td_schema_priv["events"]["behavior"]["fileSystem_utilization_high"]["forms"] = [{"href":id_priv+"/fs_util_high"}]
	td_schema_priv["events"]["behavior"]["fileSystem_utilization_medium"]["forms"] = [{"href":id_priv+"/fs_util_medium"}]
	td_schema_priv["events"]["behavior"]["fileSystem_utilization_low"]["forms"] = [{"href":id_priv+"/fs_util_low"}]
	for i in range(0,len(extras)):
		td_schema_priv["properties"]["extra"][extras[i]]["forms"] = [{"href":id_priv+"/extras/"+str(extras[i])}] 
	for i in range(0,len(extras_e)):
		td_schema_priv["events"]["extra"][extras_e[i]]["forms"] = [{"href":id_priv+"/extras/"+str(extras[i])}] 
	if actions:
		act = getActions(actions,id_global,actions_p,"private",id_priv)
		td_schema_priv["actions"] = act
	#print("\nThe private container representation has been generated \n")
	return td_schema_priv

def getPropertiesApp(containers,workspace):
	prop = {}
	for i in range(0,len(containers)):
			prop[containers[i][2]] = {"@type":"dockont:Container","description":containers[i][3],"forms":[{"href":workspace+"/container_"+containers[i][0]}]}
	return prop

def getExtraTDSchema(td_schema,app,name):
	extras = []
	extras_e = []
	try:
		with open('representation/config_files/'+str(app)+"-extra.cfg") as f:
			content = f.read()
			content = content.split("\n") 
			for i in range(0,len(content)):
				if(content[i] == "-cont"):
					cont = content[i+1]
					position1 = i
					if(cont == name):
						cont_str = ""
						cont_prop = ""
						cont_even = ""
						for x in range(position1+2,len(content)):
							if(content[x]!= "-cont"):
								cont_str = cont_str + "\n" +str(content[x])
							else:
								break
						cont_str = cont_str.split("\n")
						for j in range(0,len(cont_str)):
							if(cont_str[j] == "--properties"):
								positionp = j
								for x in range(positionp+1,len(cont_str)):
									if(cont_str[x]!= "-cont" and cont_str[x]!= "--events"):
										cont_prop = cont_prop +str(cont_str[x])
									else:
										break
							else:
								if(cont_str[j] == "--events"):
									positione = j
									for x in range(positione+1,len(cont_str)):
										if(cont_str[x]!= "-cont" and cont_str[x]!= "--events"):
											cont_even = cont_even  +str(cont_str[x])
										else:
											break

						dict_prop = ast.literal_eval(cont_prop)
						dict_even = ast.literal_eval(cont_even)
						td_schema["properties"]["extra"] = dict_prop
						td_schema["events"]["extra"] = dict_even
						extras = dict_prop.keys()
						extras_e = dict_even.keys()
						#print(extras)
						#print(extras_e)
	except IOError:
		print("The file doesnt exists")
	return td_schema,extras,extras_e

def getActions(actions,id_global,actions_p,pp,id_long):
	act = {}
	inputs_list = []
	outputs_list =[]
	actions_inp = [0] * len(actions)
	actions_out = [0] * len(actions)
	#print(actions)
	for i in range(0,len(actions)):
		act[actions[i][0]] = {"description":actions[i][1],"input":{},"output":{},"forms":[{}]}
		if(pp == "public"):
			if(actions_p[i]=="y"):
				act[actions[i][0]]["forms"] = [{"href":id_global+"/actions/"+actions[i][0],"type":actions[i][3]}]
			else:act[actions[i][0]]["forms"] = [{"href":"private"}]
		else:
			act[actions[i][0]]["forms"] = [{"href":id_long+"/"+actions[i][0]}]
		
		if(len(actions[i])>3):
			for j in range(0,len(actions[i])):
				if(isinstance(actions[i][j], list)):
					if(actions[i][j][0] == "input"):
						inputs_list.append(actions[i][j])
						actions_inp[i] = actions_inp[i] + 1
					if(actions[i][j][0] == "output"):
						outputs_list.append(actions[i][j])
						actions_out[i] = actions_out[i] + 1
			for j in range(0,len(actions[i])):
				if(len(inputs_list)>0):
					act[actions[i][0]]["input"] = {"type":"object","properties":{}}
					for l in range(0,len(inputs_list)):	
						act[actions[i][0]]["input"]["properties"][inputs_list[l][1]]={"type":inputs_list[l][2],"description":inputs_list[l][3]}
				if(len(outputs_list)>0):
					act[actions[i][0]]["output"] = {"type":"object","properties":{}}
					for l in range(0,len(outputs_list)):
						act[actions[i][0]]["output"]["properties"][outputs_list[l][1]]={"type":outputs_list[l][2],"description":outputs_list[l][3]}
		inputs_list = []
		outputs_list = []

	return act

def getDataFile(file):
	app = []
	f = open(file, "r")
	content = f.read()
	content = content.split("\n")
	app_name = content[0]
	app_description = content[1]
	app.append(app_name)
	app.append(app_description)
	conts = []
	containers = []
	actions = []
	inputs = []
	outputs = []
	for i in range(1,len(content)):
		if(content[i] == "-cont"):
			actions = []
			#print(content[i+1])
			conts.append(content[i+1])
			containers.append(content[i+1])
			containers.append(content[i+2])
			if(i+2 == len(content)-1):
				app.append(containers)
				containers = []
			else:
				if(i+2 != len(content)-1 and content[i+3] == "-cont"):
					app.append(containers)
					containers = []
		if(content[i] == "--act"):
			inputs = []
			outputs = []
			actions.append(content[i+1])
			actions.append(content[i+2])
			actions.append(content[i+3])
			actions.append(content[i+4])
			if(i+4 == len(content)-1):
				containers.append(actions)
				app.append(containers)
				containers = []
				actions = []
			else:
				if(i+4 != len(content)-1 and content[i+5] == "-cont"):
					containers.append(actions)
					app.append(containers)
					containers = []
					actions = []
				if(i+4 != len(content)-1 and content[i+5] == "--act"):
					containers.append(actions)
					actions = []
		if(content[i] == "---input"):
			inputs.append("input")
			inputs.append(content[i+1])
			inputs.append(content[i+2])
			inputs.append(content[i+3])
			actions.append(inputs)
			inputs = []
			if(i+3 == len(content)-1):
				containers.append(actions)
				app.append(containers)
			else:
				if(i+3 != len(content)-1 and content[i+4] == "--act"):
					containers.append(actions)
					actions = []
				if(i+3 != len(content)-1 and content[i+4] == "-cont"):
						containers.append(actions)
						app.append(containers)
						containers = []
						actions = []
		if(content[i] == "---output"):
			outputs.append("output")
			outputs.append(content[i+1])
			outputs.append(content[i+2])
			outputs.append(content[i+3])
			actions.append(outputs)
			outputs = []
			if(i+3 == len(content)-1):
				containers.append(actions)
				app.append(containers)
			else:
				if(i+3 != len(content)-1 and content[i+4] == "--act"):
					containers.append(actions)
					actions = []
				if(i+3 != len(content)-1 and content[i+4] == "-cont"):
					containers.append(actions)
					app.append(containers)
					containers = []
					actions = []
		
	return app,conts

def getStructureFile(file):
	app_structure = []
	if os.path.exists("representation/structure_files/"+file):
		f = open("representation/structure_files/"+file, "r")
		content = f.read()
		app_structure = content.split("\n")
	return app_structure			

def getDataInspect(name_container):
	res = os.popen("docker inspect "+name_container)
	data = json.loads(res.read())
	#print(name_container)
	id_long = data[0]["Id"]
	id_container = id_long[0:12]
	status = data[0]["State"]["Status"]
	mounts = data[0]["Mounts"]
	if not mounts:
		volumes = 0
	else:
		volumes = 1
	platform = "Docker"
	image = data[0]["Config"]["Image"]
	ports = data[0]["HostConfig"]["PortBindings"]
	entrypoint_array = data[0]["Config"]["Entrypoint"]
	entrypoint = ""
	for i in range(0,len(entrypoint_array)):
		entrypoint = entrypoint + entrypoint_array[i]+","
	docker_port = list(ports.keys())
	if docker_port:
		docker_port = docker_port[0]
		host_port = data[0]["HostConfig"]["PortBindings"][docker_port][0]["HostPort"]
	else:
		#para cuando no se especifica port en el compose	
		docker_port = "0"
		host_port = "0"
	
	return id_container,id_long,status,volumes,platform,image,docker_port,host_port,entrypoint

def getDataCont(app):
	containers_info = []
	c_info = []
	actions = []
	for i in range(2,len(app)):
		id_container,id_long,status,volumes,platform,image,docker_port,host_port,entrypoint = getDataInspect(app[i][0])
		docker_port = docker_port.split("/")
		docker_port = docker_port[0]
		c_info.extend([id_container,id_long,app[i][0],app[i][1],status,volumes,platform,image,docker_port,host_port,entrypoint])
		pp = "pub"
		if(len(app[i])>2):
			for j in range(2,len(app[i])):
				actions.append(app[i][j])
			status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p = getInfoP(str(app[i][0]),actions,pp)
			#actions = []
		else:
			status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p = getInfoP(str(app[i][0]),actions,pp)
		c_info.extend([status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p])
		c_info.append(actions)
		containers_info.append(c_info)
		c_info = []
		actions = []
	return containers_info

def getInfoP(name_cont,actions,pp):
	if(pp == "pub"):
		status_p = "y"
		image_p = "y"
		volumes_p = "y"
		utility_p = "y"
		extras_p = "y"
		extras_ep = "y"
		structure_p = "y"
		actions_p = []
		if(len(actions)>0):
			for i in range(0,len(actions)):
				actions_p.append("y")
	else:
		print("Container: "+name_cont)
		print("\n")
		print('If you want all the properties to be public write "pub", if you want them to be private write "priv", in case you want to select individually press "n":')
		prop_p = input("")
		if(prop_p == "priv"):
			status_p = "n"
			image_p = "n"
			volumes_p = "n"
			utility_p = "n"
			actions_p = []
			if(len(actions)>0):
				for i in range(0,len(actions)):
					actions_p.append("n")
		else:
			if(prop_p == "pub"):
				status_p = "y"
				image_p = "y"
				volumes_p = "y"
				utility_p = "y"
				actions_p = []
				if(len(actions)>0):
					for i in range(0,len(actions)):
						actions_p.append("y")
			else:
				print('\nPlease press "y" if you want the property public otherwise press "n" if you want the property private')
				status_p = input("\nStatus: ")
				if(status_p != "y" and status_p != "n"):
					status_p = input('\nStatus enter a valid value ("y" or "n"): ')
				image_p = input("\nImage: ")
				if(image_p != "y" and image_p != "n"):
					image_p = input('\nImage enter a valid value ("y" or "n"): ')
				volumes_p = input("\nVolumes: ")
				if(volumes_p != "y" and volumes_p != "n"):
					volumes_p = input('\nVolumes enter a valid value ("y" or "n"): ')
				utility_p = input("\nUtilization Factors (CPU, Memory, Network FileSystem): ")
				if(utility_p != "y" and utility_p != "n"):
					utility_p = input('\nUtilization Factors enter a valid value ("y" or "n"): ')
				actions_p = []
				if(len(actions)>0):
					for i in range(0,len(actions)):
						act_p = input('\nAction "'+actions[i][0]+'": ')
						if(act_p != "y" and act_p != "n"):
							act_p = input('\nAction "'+actions[i][0]+'": enter a valid value ("y" or "n"): ')
						actions_p.append(act_p)
	return status_p,image_p,volumes_p,utility_p,extras_p,extras_ep,structure_p,actions_p

def getJsonStructure(nodes,edges):
	nod = []
	edg = []
	for i in range(0,len(nodes)):
		n = []
		n.append(nodes[i])
		n.append(nodes[i])
		nod.append(n)
	for i in range(0,len(edges)):
		c = edges[i].split("-")
		n = []
		n.append(c[0])
		n.append(c[1])
		edg.append(n)
	json_str = {"data":{}}
	json_str["data"]["nodes"] = nod
	json_str["data"]["edges"] = edg
	return json_str

def getExtras(file):
	extras = []
	if os.path.exists("representation/config_files/"+file):
		f = open("representation/config_files/"+file, "r")
		content = f.read()
		content = content.split("\n")
		for i in range(0,len(content)):
			if(content[i]=="-cont"):
				name_cont = content[i+1]
				position = i
				extras_prop = []
				extras_eve = []
				if(content[i+2]=="--properties"):
					for j in range(position+3,len(content),2):
						if(content[j] != "--events"):
							extras_prop.append(name_cont)
							extras_prop.append("p")
							extras_prop.append(content[j])
							extras_prop.append(content[j+1])
							extras.append(extras_prop)
							extras_prop = []
						else:
							pp = j
							break
				if(content[pp]=="--events"):
					for j in range(pp+3,len(content),2):
						if(content[j] != "--properties"):
							extras_eve.append(name_cont)
							extras_eve.append("e")
							extras_eve.append(content[j])
							extras_eve.append(content[j+1])
							extras.append(extras_eve)
							extras_eve = []
						else:
							break
	return extras

service_name = sys.argv[1]
file_cfg = service_name

dir = os.path.dirname(file_cfg) + "/"


app, conts = getDataFile(file_cfg)

app_name = app[0]
app_description = app[1]

containers_info = getDataCont(app)

extras = getExtras(app_name+"-extra-info.cfg")
app_structure = getStructureFile(app_name+"-structure.cfg")

json_structure = getJsonStructure(conts,app_structure)

app_td_schema = generateTDSchemaApp(app[0],app[1],containers_info)

containers_info = generateTDSchemasConts(app_name,containers_info)

#print(containers_info)

storeValuesApp(app_name,app_description,containers_info,app_td_schema,json_structure,extras, dir)

print("The representation has already been generated")
