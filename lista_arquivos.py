import requests

class Projeto:
    def __init__(self, name, identity):
        self.nome = name
        self.ident = identity
        self.items = []

class Conteudo:
    def __init__(self, name, identity):
        self.tipos = ['Pasta', 'Arquivo']
        self.tipo = ""
        self.nome = name
        self.ident = identity
        self.items = []
    def set_tipo(self,ind):
        self.tipo = self.tipos[ind]

projetos = []

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

resposta_pjt = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/"+hubId+"/projects", token)

for element in resposta_pjt['data']:
    if element['type'] == 'projects':
        pjt = Projeto(element['attributes']['name'], element['id'])
        projetos.append(pjt)
    else:
        pass

def subpastas(projeto, pasta):
    resposta_obj = getRespJson("https://developer.api.autodesk.com/data/v1/projects/"+projeto.ident+"/folders/"+pasta.ident+"/contents", token)
    for content in resposta_obj['data']:
        if content['type'] == 'folders':
            contenido = Conteudo(content['attributes']['name'], content['id'])
            contenido.set_tipo(0)
            pasta.items.append(contenido)
            subpastas(projeto, contenido)
        else:
            contenido = Conteudo(content['attributes']['displayName'], content['id'])
            contenido.set_tipo(1)
            pasta.items.append(contenido)

for pjt in projetos:
    resposta_pasta = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/"+hubId+"/projects/"+pjt.ident+"/topFolders", token)
    for topfolder in resposta_pasta['data']:
        if topfolder['type'] == 'folders': 
            cont = Conteudo(topfolder['attributes']['name'], topfolder['id'])
            cont.set_tipo(0)
            pjt.items.append(cont)
            subpastas(pjt, cont)
        else:
            cont = Conteudo(topfolder['attributes']['name'], topfolder['id'])
            cont.set_tipo(1)
            pjt.items.append(cont)

def conteudos(pasta):
    for conteudo in pasta.items:
        if conteudo.tipo == 'Pasta':
            print(conteudo.nome)
            conteudos(conteudo)
        else:
            print(conteudo.nome)

for projeto in projetos:
    print("Projeto: "projeto.nome)
    for element in projeto.items:
        if element.tipo == 'Pasta':
            conteudos(element)
        else:
            print(element.nome)