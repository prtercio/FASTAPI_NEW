import odoolib

#url = "http://localhost:8069"
#db = 'db_prueba'
#username = 'prtercui@gmail.com'
#password = 'Tcad070819'

""" url = "http://10.20.30.100:8206”
db = ‘ntec’
username = 'soporte@ntec.com.mx'
password = '!Coron321!' """

connection = odoolib.get_connection(
    hostname="10.20.30.100",
    database="ntec",
    login="soporte@ntec.com.mx",
    password="!Coron321!",
    port=8206,
    protocol="jsonrpc"
) 
""" connection = odoolib.get_connection(
    hostname="localhost",
    database="db_prueba",
    login="prtercui@gmail.com",
    password="Tcad070819",
    port=8069,
    protocol="jsonrpc"
) """

country_model = connection.get_model('res.country')
country_id = country_model.search([('name','=','United States')])[0]
partner_model = connection.get_model('res.partner')
partner = partner_model.create({
    'name':'Samuel Martinez',
    'street':'Guadalupe',
    'zip':'64800',
    'city':'Mty',
    'country_id':country_id,
    'phone':'93438483483',
    'email':'samuelmart@gmail.com'
}) 


producto_syscom = 'Power Bean Syscom'

product_model = connection.get_model('product.product')
car_product = product_model.create({
    'name':producto_syscom,
    'type':'consu',
    'categ_id':1,
    'list_price':15000,
    'standard_price':20000
})

crm_model = connection.get_model('crm.lead')
crm_order = crm_model.create({
    'name':'Oportunidad Samuel Martinez',
    'type':'opportunity',
    'partner_id':partner
})

so_model = connection.get_model('sale.order')
sale_order = so_model.create({
    'partner_id':partner,
    'opportunity_id':crm_order,
    'order_line':[(0,0, {
        'product_id':car_product,
        'product_uom_qty':1
    })]
    
})


crm_model = connection.get_model('crm.lead')
crm_order = crm_model.create({
    'name':'Alef Benyamin',
    'type':'opportunity',
    'partner_id':partner
})