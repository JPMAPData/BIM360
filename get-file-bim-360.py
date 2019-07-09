import requests #http://requests.readthedocs.org/en/latest/

def getToken(client_id, client_secret):
    """Obtain Forge token given a client id & secret"""
    req = { 'client_id' : client_id, 'client_secret': client_secret, 'grant_type' : 'client_credentials','scope':'data:read'}
    resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json();
    #return resp['token_type'] + " " + resp['access_token']
    return resp['access_token']
  
token = getToken("Dm1AJ95famLKnf4MUOGpwO7zJIcBF4J7", "vAyaauIpMr4qhy6O")

def getRespJson(url, token):
    headers = {'Authorization': 'Bearer ' + token}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    if resp.status_code == 200:
        return resp.json()
    else:
        return resp.status_code

def getHubId(jason):
    return jason['data'][0]['id']

resposta_hub = getRespJson("https://developer.api.autodesk.com/project/v1/hubs", token)

hubId = getHubId(resposta_hub)

print ("ID do Hub : "+hubId)

resposta_pjt = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/"+hubId+"/projects", token)

nome_pjt = "My Project"

def getProjectId(jason, nome_projeto):
    for data in jason['data']:
        if data['type']=="projects" and data['attributes']['name'] == "My Project":
            return data['id']
        else:
            pass

id_pjt = getProjectId(resposta_pjt, nome_pjt)

print ("ID do projeto : "+id_pjt) 

resposta_pasta = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/"+hubId+"/projects/"+id_pjt+"/topFolders", token)

def getFolderId(jason, nome_pasta):
    for data in jason['data']:
        if data['type']=="folders" and data['attributes']['name'] == nome_pasta:
            return data['id']
        else:
            pass

nome_pasta = "Project Files"

id_pasta = getFolderId(resposta_pasta, nome_pasta)

resposta_obj = getRespJson("https://developer.api.autodesk.com/data/v1/projects/"+id_pjt+"/folders/"+id_pasta+"/contents", token)

nome_arq = "base.nwd"

def getObjId(jason, nome_arq):
    for data in jason['included']:
        if data['attributes']['displayName'] == nome_arq:
            return data['relationships']['storage']['data']['id']
        else:
            pass

id_arq = getObjId(resposta_obj, nome_arq)

print ("ID do objeto : "+id_arq)

def getBktKeynObjName(id_arquivo):
    lista = id_arquivo.split('/')
    bucket_key = lista[0].split(':')[3]
    object_name = lista[1]
    return {"bucket key":bucket_key,"object name":object_name}
    
bktKeynObjName = getBktKeynObjName(id_arq)

print("bucket key : "+bktKeynObjName['bucket key'])

print("object name : "+bktKeynObjName['object name'])

def downloadFile(download_url, nome_arquivo, token):
    headers = {'Authorization': 'Bearer ' + token}
    resp = requests.get(download_url, headers = headers)
    resp.raise_for_status()
    if resp.status_code == 200:
        open(nome_arquivo, 'wb').write(resp.content)
    else:
        pass

downloadFile("https://developer.api.autodesk.com/oss/v2/buckets/"+bktKeynObjName['bucket key']+"/objects/"+bktKeynObjName['object name'], "Teste_Python.nwd", token)
