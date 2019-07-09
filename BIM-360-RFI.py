# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:17:16 2019
@author: joao.martins
"""

import requests

def getToken(client_id, client_secret):
    """Obtain Forge token given a client id & secret"""
    req = {'client_id' : client_id, 'client_secret': client_secret, 'grant_type' : 'client_credentials','scope':'data:read'}
    resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json();
    return resp['access_token']

token = getToken("LK6GFWK7zVTftQnlZQfk6GTBkZkHYaXj", "jAyVk6JsG13t8WWE")

print (token)


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

print ('Hub Id: ' +hubId)

resposta_pjt = getRespJson("https://developer.api.autodesk.com/project/v1/hubs/"+hubId+"/projects", token)

nome_pjt = "Zanaki -"

def getRfisId(jason, nome_projeto):
    for data in jason['data']:
        if data['attributes']['name'] == nome_projeto:
            saida = data['relationships']['rfis']['data']['id']
        else:
            pass
    return saida

id_rfis = getRfisId(resposta_pjt, nome_pjt)

print ('RFIs container Id: '+id_rfis)

def getRfis(token, RIF_Id):
    headers = {'Authorization':'Bearer '+token}
    resp = requests.get("https://developer.api.autodesk.com/issues/v1/containers/"+RIF_Id+"/quality-issues", headers = headers)
    resp.raise_for_status()
    if resp.status_code == 200:
        return resp.json()
    else:
        return resp.status_code

rfis = getRfis(token, id_rfis)

print (rfis)
