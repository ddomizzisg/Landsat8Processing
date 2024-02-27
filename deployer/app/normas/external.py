import requests #python -m pip install requests, doc: https://docs.python-requests.org/en/latest/user/quickstart/
import checklists_final
import json

API_CONTAINERS = "http://148.247.201.222:5001/containers/container_{container_id}/info"


def query_api(api_link, data):
    try:
        api_link = api_link.format(container_id=data)
        r = requests.get(api_link, timeout=2)
        return json.loads(r.text)
    except Exception as inst:
        return ""

def api_call_resolver(source, data):
    #define API target
    api_link = ""
    if source == checklists_final.SOURCE_API_CONTAINERS:
        api_link = API_CONTAINERS
    #call API
    responses = []
    for dat in data:
        response = query_api(api_link, dat)
        if response:
            responses.append(response)
    return responses



# container_id = "2ddadadc932532be1d555e67ce167dd4607af18a841b682b0bb777041638ac2f"
# print(query_api(API_CONTAINERS, "abf94365cfa4650593aaf4561d7fb9fca9e103602cc7df594b2efc065cda8eb4"))