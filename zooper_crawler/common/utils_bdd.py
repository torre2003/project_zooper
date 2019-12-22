# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#!/usr/bin/python
import json
import psycopg2
from datetime import datetime

hostname = 'localhost'
username = 'USERNAME'
password = 'PASSWORD'
database = 'DBNAME'

DATABASES = {
    'zooper_local': {
        'NAME': 'zooper_matching',  # os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'zooper',
        'PASSWORD': 'asdf1234',
        'HOST': '127.0.0.1',  # 127.0.0.1, localhost, ...
        'PORT': '5432',  # 3306 (mysql), 5432 (postgresql), ...
    }
}

def extraer_datos_bdd(nombre=None):
    if nombre is None:
        nombre = DATABASES.keys()[0]
    return DATABASES[nombre]

def ejecutar_consulta(consulta,nombre_bdd=None):
    bdd=extraer_datos_bdd(nombre_bdd)
    resutaldos = 'resultados_vacios'
    with psycopg2.connect( 
            host=bdd['HOST'], 
            user=bdd['USER'], 
            password=bdd['PASSWORD'], 
            dbname=bdd['NAME']
                    ) as connexion:
        with connexion.cursor() as cursor:
            cursor.execute(consulta)
            resultados = dictfetchall(cursor)
    connexion.close()
    return resultados

def ejecutar_update(consulta,nombre_bdd=None):
    bdd=extraer_datos_bdd(nombre_bdd)
    with psycopg2.connect( 
            host=bdd['HOST'], 
            user=bdd['USER'], 
            password=bdd['PASSWORD'], 
            dbname=bdd['NAME']
                    ) as connexion:
        with connexion.cursor() as cursor:
            cursor.execute(consulta)
    connexion.close()
    return 

def dictfetchall(cursor):
    #"Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def ingresar_registro_temporal (data):
    """
        Funcion para ingresar un registro temporal a la tabla comunicacion_scrapy
        para su post proceso en zooper_matching
        params
            diccionario o string json con la información a enviar
        return 
            codigo único de la tupla

    """
    #INSERT INTO comunicacion_scrapy ("codigo", "data") VALUES ('COD','{"data":"data"}'::json)
    now = datetime.now()
    codigo = unicode(now.year)+\
        unicode(now.month)+\
        unicode(now.day)+\
        unicode(now.hour)+\
        unicode(now.minute)+\
        unicode(now.second)+\
        unicode(now.microsecond)
    if type(data) == type("string"):
        pass
    elif type(data) == type({}):
        data = json.dumps(data,ensure_ascii=False)
    else:
        return
    query = """INSERT INTO comunicacion_scrapy ("codigo", "data") VALUES ('{}','{}'::json);""".format(codigo, data)
    ejecutar_update(query)
    return codigo

