# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:29:24 2019

@author: joao.martins
"""

import requests

def getToken(client_id, client_secret):
    """Obtain Forge token given a client id & secret"""
    req = { 'client_id' : client_id, 'client_secret': client_secret, 'grant_type' : 'client_credentials','scope':'data:create'}
    resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json()
    #return resp['token_type'] + " " + resp['access_token']
    return resp['access_token']

token = getToken("Dm1AJ95famLKnf4MUOGpwO7zJIcBF4J7", "V050fdb1761e4460")

headers = {'Authorization': token,'Content-Type': 'application/vnd.api+json'}

data = '{"jsonapi": {"version": "1.0"},"data":{"type": "folders","attributes": {"name": "Criada","extension": {"type": "folders:autodesk.bim360:Folder","version": "1.0"}},"relationships": {"parent": {"data": {"type": "folders","id": "urn:adsk.wipprod:fs.folder:co.daQkem-CTT-Am6rC_FmHCg"}}}}}'

response = requests.post('https://developer.api.autodesk.com/data/v1/projects/b.3b5c6352-cf34-41fd-a0e9-a5246d93bf55/folders', headers=headers, data=data)

print(token)
print(response)