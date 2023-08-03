#SYSCOM
import requests
from requests.structures import CaseInsensitiveDict
import json

url = "https://developers.syscom.mx/api/v1/productos"

headers = CaseInsensitiveDict()
headers["Authorization"] = "Bearer  token"

equipo = 'PowerBeam airMAX'

paylodad = {'busqueda': equipo}
resp = requests.get(url, headers=headers, params=paylodad)

r_dict = resp.json()


jsn_list = json.loads(json.dumps(r_dict['productos'])) 
for lis in jsn_list:    
    for key,val in lis.items():
        if key == "producto_id":
            print(key," = ", val,)
        if key == "modelo":
            print(key," = ", val,)
        if key == "titulo":
            print(key," = ", val,)
        if key == "marca":
            print(key," = ", val) 
    print('Precio: ',lis['precios']['precio_1'])
    print('Proveedor: ',lis['precios']['precio_descuento'])
    print("--------------------")
        
        
#print(r_dict['productos'][0]['titulo'])
#print(r_dict['productos'][0]['precios']['precio_descuento'])
#print(r_dict['productos'][0]['precios']['precio_1'])
