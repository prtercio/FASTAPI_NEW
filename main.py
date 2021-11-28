import xmlrpc.client

from typing import Optional

from fastapi import FastAPI

from config import config_

from pydantic import BaseModel


###########
# para correr o servidor ejecutar el comando uvicorn main:app --reload
#################


# url = "http://10.20.30.100:8031"
# db = 'V-Lumber'
# username = 'systems.admin@v-lumber.com'
# password = 'Fenix#858'
url = "http://localhost:8069"
db = 'db_prueba'
username = 'prtercui@gmail.com'
password = 'Tcad070819'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})
print(uid)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

class User(BaseModel):
    name : str
    street: str
    website: str

### EJEMPLO DE TAGS METADATA
tags_metadata =[
    {
        "id":"Id Product", 
        "name":"Products", 
        "type":"Type of product", 
        "list_price":"Price", 
        "taxes_id":"Taxes",
        "sale_ok":"Active"
    },
    {
                "name":"Locations",
                'id': 'Id Location',
                'location_dest_id': "Location dest",
                'product_id': "Product id",
                'qty_done': "Quantity",
                'date': "Date"
    },
    {"name":"Peliculas", "descritpion":"Product Odoo List"}
]

app = FastAPI(
    title=config_.TITLE,
    version=config_.VERSION,
    description=config_.DESCRIPTION,
    openapi_tags=tags_metadata,
    contact = {"name":config_.NAME, "email":config_.EMAIL}
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/lista/{item}")
async def read_items(item):
    return [{"item_id": item}]

#get contact odoo (productId = id_contact ) #################################################################
@app.get('/api/v1/product/{productId}', tags=["Products"])
async def ProductId(productId):
    #new_id = int(UserId)
    ids = models.execute_kw(db, uid, password,
    'product.template', 'search',
    [[['id','=',productId]]])
    list_productId = models.execute_kw(db, uid, password, 'product.template', 'read', [ids],
{'fields': ['id', 'name','type', 'list_price', 'taxes_id', 'sale_ok']})
    #request = {'id': user_data[0]['id'], 'name': user_data[0]['name'], 'street': user_data[0]['street'],'website': user_data[0]['website']}
    return list_productId

#get products activos #################################################################
@app.get('/api/v1/products/', tags=["Products"])
async def products():

    ids = models.execute_kw(db, uid, password,
    'product.template', 'search',
    [[['sale_ok','=',True]]])
    print('=========== ',ids)
    lista_data = models.execute_kw(db, uid, password, 'product.template', 'read', [ids],
{'fields': ['id', 'name','type', 'list_price', 'taxes_id', 'sale_ok']})
    list_products = []
    for item in lista_data:
        list_products.append(
            {
                'id': item['id'],
                'name': item['name'],
                'type': item['type'],
                'list_price': item['list_price'],
                'taxes_id': item['taxes_id'][0]
            }
        )
    return list_products

#get ventas activos #################################################################
@app.get('/api/v1/sales/')
async def salesList():

    ids = models.execute_kw(db, uid, password,
    'sale.order', 'search',
    [[['partner_id','=',7]]])
    print('=========== ',ids)
    lista_data = models.execute_kw(db, uid, password, 'sale.order', 'read', [ids],
{'fields': ['id', 'name','partner_id', 'date_order', 'order_line']})
    new_sales = []
    for item in lista_data:
        new_sales.append(
            {
                'id': item['id'],
                'name': item['name'],
                'date_order': item['date_order'],
                'order_line': item['order_line']
            }
        )
    return new_sales

#get peliculas activos #################################################################
@app.get('/api/v1/peliculas/', tags=["Peliculas"])
async def pelisList():

    ids = models.execute_kw(db, uid, password,
    'presupuesto', 'search',
    [[['active','=',True]]])
    print('=========== ',ids)
    lista_data = models.execute_kw(db, uid, password, 'presupuesto', 'read', [ids],
{'fields': ['id', 'name','clasificacion', 'puntuacion', 'genero_ids', 'director_id' ]})
    new_peliculas = []
    for item in lista_data:
        new_peliculas.append(
            {
                'id': item['id'],
                'name': item['name'],
                'clasificacion': item['clasificacion'],
                'puntuacion': item['puntuacion'],
                'genero_ids': item['genero_ids'],
                'director_id': item['director_id']
            }
        )
    return new_peliculas

#get contact odoo (UserId = id_contact ) #################################################################
@app.get('/api/v1/user/<string:UserId>', tags=["Locations"])
def userId(UserId):
    new_id = int(UserId)
    ids = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['id', '=', new_id]]],
    {'limit': 1})
    user_data = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids],
{'fields': ['id', 'name', 'street', 'website']})
    return user_data


@app.post("/api/v1/user", tags=["Locations"])
def postUser(user : User):
    id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
        "name": "Alejandro1",
        "street": "Monterrey1",
        "website": "ntec.com1"
    }])
    


#get location x_studio_field_2vUVw #################################################################
@app.get('/api/v1/locations/<string:UserId>', tags=["Locations"])
def UserIdlocation(UserId):
    new_id = int(UserId)
    ids = models.execute_kw(db, uid, password,'stock.location', 'search',[[['x_studio_field_2vUVw', '=', new_id]]])
    location_data = models.execute_kw(db, uid, password, 'stock.location', 'read', [ids], {'fields': ['id', 'name','complete_name', 'active', 'location_id','x_studio_field_2vUVw']})

    new_locations = []
    for item in location_data:
        new_locations.append(
            {
                'location_dest_id': item['id'],
                'location': item['name'],
                'complete_name': item['complete_name'],
                'active': item['active'],
                'location_id': item['location_id'][0]
            }
        )
    return new_locations


#get producto stock.move.line #################################################################
@app.get('/api/v1/products/<string:location_id_move>', tags=["Locations"])
def ProductsMove(location_id_move):
    new_id = int(location_id_move)
    ids = models.execute_kw(db, uid, password,'stock.move.line', 'search',[[['location_dest_id', '=', new_id]]])
    products_data = models.execute_kw(db, uid, password, 'stock.move.line', 'read', [ids], {'fields': ['id', 'location_dest_id','product_id', 'qty_done', 'date']})

    new_products = []
    for item in products_data:
        new_products.append(
            {
                'id': item['id'],
                'location_dest_id': item['location_dest_id'][0],
                'product_id': item['product_id'],
                'qty_done': item['qty_done'],
                'date': item['date']
            }
        )
    return new_products

#get CRM #################################################################
# 
