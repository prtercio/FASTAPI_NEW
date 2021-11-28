#SYSCOM
import requests
from requests.structures import CaseInsensitiveDict
import json

url = "https://developers.syscom.mx/api/v1/productos"

headers = CaseInsensitiveDict()
headers["Authorization"] = "Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijk3Mjc1ZjcwZDRmZDI0ZDk3ZGJiODllM2I0ZmQwZmUzNDk4NGVkYmFmZjY0Zjg3MzhhODYyMmQ4MzRmZTAwZTQ3MTUwNDk3NTVkMjNkNjcxIn0.eyJhdWQiOiIzS0dGSVN4V3d0RFhVQWVkUXo3eHFxQkZXS3hNcGRKaiIsImp0aSI6Ijk3Mjc1ZjcwZDRmZDI0ZDk3ZGJiODllM2I0ZmQwZmUzNDk4NGVkYmFmZjY0Zjg3MzhhODYyMmQ4MzRmZTAwZTQ3MTUwNDk3NTVkMjNkNjcxIiwiaWF0IjoxNjMzNzk4NDk4LCJuYmYiOjE2MzM3OTg0OTgsImV4cCI6MTY2NTMzNDQ5OCwic3ViIjoiIiwic2NvcGVzIjpbXX0.sScIubVsKbxqqEExIPzd6-ucQU9GCAX--RnwiBuMGazczFpwAPBB_QXOKHaMz6TYftIIzmjl9jDpnRa4XMrGJvMCAQgJNpGF5ySpQ22sE0LaolihtNdPj-JFN1zAeJ71Sql7YIe516etoCLJy0U_eLlpwK2ZqwF1s7aZFG-NCpsaXV2kREIfHjAq71Ywv55V8me8pF94W-biF1g65flN8nufpMmrPidas2KcgelOOm0d521keX9948tNBFdQULMqqsBuxRuu9RtZdL0ehy5qEJkK7Iw8V19EtxqGqdmXo6do-wX9AmOcxExOiVX4ks0p3QsIgbjK1o_tkJgj5XOITR6wzqnw3P3zceoarqUmBB5RXZBPHRaqf3SuCI7eGVcZa8eeAIar-xT95Q59U7D2iRMID4KYPH-O00wirnJpa8Py2PCN4iYgDfJYzV1ouB2bgbxhyZLjn0DZLyKYym12rZ3SwrR0XOl0NZALHZVrAu-jupf3mDd_uYteak5SZRWbsapxm_HRokdVd-WhG8H_0K8TjtGcCLJI6wc2Z1aGFz-U9DNkSnLz1fBcsCnS9xwCoZYrQJ6HZestlRAhEnlNinudxt8vzPjbTozGhlYzvme_rYM6BNdPa7UTlSUu44Y0SOEmxzTZr8p9VgXf9NsjItULvZKQr6qOS0CTNYzA1Bk"

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
