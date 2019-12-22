# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import urllib3




def consultar_productos_a_actualizar():
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://127.0.0.1:8888/producto/obtener_productos_a_actualizar_json/')
    data = json.loads(r.data.decode('utf-8'))
    return data


def enviar_actualizacion_producto(cod_supermercado, supermercado, precio, status_actualizacion, **extra_params):
    http = urllib3.PoolManager()
    url = 'http://127.0.0.1:8888/producto/actualizacion_registro_producto_json/?cod_supermercado={}&supermercado={}&precio={}&status_actualizacion={}'.format(
        cod_supermercado,supermercado,precio,status_actualizacion)
    extras = ''
    for param in extra_params:
        extras = extras+'&{}={}'.format(param, extra_params[param])
    url = url + extras
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    return data


def consultar_productos_custom(supermercado, **extra_params):
    http = urllib3.PoolManager()
    url = 'http://127.0.0.1:8888/producto/obtener_productos_custom_json/?supermercado={}'.format(supermercado)
    extras = ''
    for param in extra_params:
        extras = extras+'&{}={}'.format(param, extra_params[param])
    url = url + extras
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    return data


def enviar_actualizacion_producto_custom(cod_supermercado, supermercado, status_actualizacion, params, **extra_params):
    http = urllib3.PoolManager()
    url = 'http://127.0.0.1:8888/producto/actualizacion_producto_custom_json/?cod_supermercado={}&supermercado={}&status_actualizacion={}&params={}'.format(cod_supermercado,supermercado,status_actualizacion,params)
    extras = ''
    for param in extra_params:
        extras = extras+'&{}={}'.format(param, extra_params[param])
    url = url + extras
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    print data
    return data



def consultar_articulo_supermercado_custom(supermercado, **extra_params):
    http = urllib3.PoolManager()
    url = 'http://127.0.0.1:8888/supermercado/obtener_articulos_supermercados_json?supermercado={}'.format(supermercado)
    # url = 'http://127.0.0.1:8888/producto/obtener_productos_custom_json/?supermercado={}'.format(supermercado)
    extras = ''
    for param in extra_params:
        extras = extras+'&{}={}'.format(param, extra_params[param])
    url = url + extras
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    return data


def ingresar_articulo_supermercado_custom(supermercado, **extra_params):
    http = urllib3.PoolManager()
    # r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json?')
    url = 'http://127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json?supermercado={}'.format(supermercado)
    extras = ''
    for param in extra_params:
        extras = extras+'&{}={}'.format(param, extra_params[param])
    url = url + extras
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    return data



# INSERT INTO comunicacion_scrapy (data) VALUES ('{"col1": "a","col2": 6,"col3": 7,"col4": "eight"}'::jsonb)