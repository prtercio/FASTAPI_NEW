import xmlrpc.client

from typing import Optional

from fastapi import FastAPI, Path

from config import config_

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware




###########
# para correr o servidor ejecutar el comando uvicorn main:app --reload
#################

url = "http://localhost:8069"
db = 'db_prueba'
username = 'prtercui@gmail.com'
password = 'Tcad070819'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

app = FastAPI(
    title=config_.TITLE,
    version=config_.VERSION,
    description=config_.DESCRIPTION,
    contact = {"name":config_.NAME, "email":config_.EMAIL}
)
class Game(BaseModel):
    name : str
    senha: str
    contacto_id: int
    game_tipo_id: int

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Info": "Api Games Biblico"}


#get todas las preguntas #################################################################
@app.get('/api/v1/perguntas/', tags=["AllPerguntas"])
async def perguntas():

    ids = models.execute_kw(db, uid, password,
    'g_p_lista.g_p_lista', 'search',
    [[['ativa','=',True]]])
    lista_data = models.execute_kw(db, uid, password, 'g_p_lista.g_p_lista', 'read', [ids],
{'fields': ['id', 'pergunta','respostaA', 'respostaB', 'respostaC', 'respostaD', 'respostaCorreta', 'dificuldade_ids', 'idioma_pregunta_ids']})
    list_perguntas = []
    for item in lista_data:
        list_perguntas.append(
            {
                'id': item['id'],
                'pergunta': item['pergunta'],
                'respostaA': item['respostaA'],
                'respostaB': item['respostaB'],
                'respostaC': item['respostaC'],
                'respostaD': item['respostaD'],
                'respostaCorreta': item['respostaCorreta'],
                'dificuldade_ids': item['dificuldade_ids'],
                'idioma_pregunta_ids': item['idioma_pregunta_ids'],

            }
        )
    return list_perguntas


#get uma pergunta #################################################################
@app.get('/api/v1/perguntas/{perguntaId}', tags=["AllPerguntas"])
async def perguntasId(perguntaId):
    ids = models.execute_kw(db, uid, password,
    'g_p_lista.g_p_lista', 'search',
    [[['id','=',perguntaId]]])
    list_productId = models.execute_kw(db, uid, password, 'g_p_lista.g_p_lista', 'read', [ids],{'fields': ['id','pergunta','respostaA', 'respostaB', 'respostaC', 'respostaD', 'respostaCorreta', 'dificuldade_ids', 'idioma_pregunta_ids']})
    return list_productId

#get perguntas por id e dificuldade ?????? #################################################################
@app.get("/api/v1/perguntas/{perguntaId}/dificuldade/{dificuldadeIds}")
async def perguntasporIddificuldades(
    perguntaId: int, dificuldadeIds: int, q: Optional[str] = None, short: bool = False
):
    ids = models.execute_kw(db, uid, password, 'g_p_lista.g_p_lista', 'search',[[['id','=',perguntaId],['dificuldade_ids','=',dificuldadeIds]]])
    list_productId_ = models.execute_kw(db, uid, password, 'g_p_lista.g_p_lista', 'read', [ids],{'fields': ['id', 'pergunta','respostaA', 'respostaB', 'respostaC', 'respostaD', 'respostaCorreta', 'dificuldade_ids', 'idioma_pregunta_ids']})
    return list_productId_

#get perguntas por dificuldades #################################################################
@app.get('/api/v1/perguntas/{dificuldade}')
async def perguntasdificuldades(dificuldade):
    ids = models.execute_kw(db, uid, password,'g_p_lista.g_p_lista', 'search',[[['dificuldade_ids','=',dificuldade]]])
    list_productId = models.execute_kw(db, uid, password, 'g_p_lista.g_p_lista', 'read', [ids],{'fields': ['id', 'pergunta','respostaA', 'respostaB', 'respostaC', 'respostaD', 'respostaCorreta', 'dificuldade_ids', 'idioma_pregunta_ids']})
    return list_productId

#post criando jogo ##################################################
@app.post("/api/v1/gameCreate/", tags=["Create"])
def postGame(game: Game):
    id = models.execute_kw(db, uid, password, 'game_biblico.game_biblico', 'create', [
        game
    ])
    return game

