# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json 
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# from django.core.paginator import Paginator

from framework_jumbo import ManagerArticuloJumbo
from common import utils
from apps import JumboConfig


def lista_articulos_view(request):
    context = {}
    return render(request,JumboConfig.name+'/lista_articulos.html',context)


def lista_articulos_json(request):
    datos = json.loads(request.POST.get('datos'))
    respuesta = {
        'paginacion':None,
        'data':None,
        'columnas':None,
        'status':None,
        'mensaje':None,#[{type:'error|success|'<- segun swal,text:'' }]
    }
    articulos = ManagerArticuloJumbo.obtenerArticulos().order_by('id')
    elementos_por_pagina = 20
    if 'elementos_por_pagina' in datos:
        elementos_por_pagina = int(datos['elementos_por_pagina'])
    numero_pagina_actual = 1
    if 'pagina' in datos:
        numero_pagina_actual = int(datos['pagina'])
    if 'marca' in datos:
        if datos['marca']:
            articulos = articulos.filter(marca__icontains=datos['marca'])
    if 'producto_id' in datos:
        if datos['producto_id']:
            articulos = articulos.filter(producto_id=datos['producto_id'])
    if 'nombre' in datos:
        if datos['nombre']:
            articulos = articulos.filter(nombre__icontains=datos['nombre'])

    elementos_pagina, paginacion = utils.paginacion_comun (articulos, elementos_por_pagina=elementos_por_pagina, pagina=numero_pagina_actual)
    columnas = []
    columnas.append({'title':'Ver', 'data':'ver'});
    columnas.append({'title':'ID Interna', 'data':'id'});
    columnas.append({'title':'P_ID Jumbo', 'data':'producto_id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Marca', 'data':'marca'});
    columnas.append({'title':'Precio', 'data':'precio'});
    columnas.append({'title':'Precio sin descuento', 'data':'precio_sin_descuento'});
    columnas.append({'title':'Imagen', 'data':'imagen'});
    columnas.append({'title':'Link', 'data':'link'});
    data_table = []
    for elemento in elementos_pagina:
        aux = {}
        aux['ver'] = '<button name="mostrar_elemento" elemento_id="'+unicode(elemento.id)+'">Ver</button>'
        aux['id'] = unicode(elemento.id)
        aux['producto_id'] = unicode(elemento.producto_id)
        aux['nombre'] = elemento.nombre
        aux['marca'] = elemento.marca
        aux['precio'] = elemento.precio
        aux['precio_sin_descuento'] = elemento.precio_sin_descuento
        aux['imagen'] = '<img src="'+elemento.url_imagen+'" style="width: 100px;height: 100px;">'
        aux['link'] = '<a href="'+elemento.url_producto+'" target="_blank">LINK</a>'
        data_table.append(aux)
    respuesta['paginacion']=paginacion
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


def ver_articulo_json(request):
    datos = json.loads(request.POST.get('datos'))
    respuesta = {
        'data':[],
        'columnas':[],
        'status':'success',
        'mensaje':None,#[{type:'error|success|'<- segun swal,text:'' }]
    }
    articulo = None
    if 'elemento_id' in datos:
        if datos['elemento_id']:
            articulo = ManagerArticuloJumbo.obtenerArticulo(int(datos['elemento_id']))
    if articulo is None:
        respuesta['mensaje'] = [{'type':'error', 'text':'No existe el articulo' }]
        respuesta['status'] = 'error'
        return JsonResponse(respuesta)
    columnas = []
    columnas.append({'title':'°', 'data':'col_0'});
    columnas.append({'title':'Característica', 'data':'col_1'});
    columnas.append({'title':'Detalle', 'data':'col_2'});

    data_table = []
    data_table.append({'col_0':0, 'col_1':'ID','col_2':unicode(articulo.id)})
    data_table.append({'col_0':1, 'col_1':'producto_id','col_2':unicode(articulo.producto_id)})
    data_table.append({'col_0':2, 'col_1':'codigo_referencia','col_2':unicode(articulo.codigo_referencia)})
    data_table.append({'col_0':3, 'col_1':'item_id','col_2':unicode(articulo.item_id)})
    data_table.append({'col_0':4, 'col_1':'ean','col_2':unicode(articulo.ean)})
    data_table.append({'col_0':5, 'col_1':'nombre','col_2':unicode(articulo.nombre)})
    data_table.append({'col_0':6, 'col_1':'marca','col_2':unicode(articulo.marca)})
    data_table.append({'col_0':7, 'col_1':'url_imagen','col_2':unicode(articulo.url_imagen)})
    data_table.append({'col_0':8, 'col_1':'url_producto','col_2':unicode(articulo.url_producto)})
    data_table.append({'col_0':9, 'col_1':'data_producto','col_2':unicode(articulo.data_producto)})
    data_table.append({'col_0':10, 'col_1':'data_sku','col_2':unicode(articulo.data_sku)})
    data_table.append({'col_0':11, 'col_1':'precio','col_2':unicode(articulo.precio)})
    data_table.append({'col_0':12, 'col_1':'precio_sin_descuento','col_2':unicode(articulo.precio_sin_descuento)})
    data_table.append({'col_0':13, 'col_1':'validez_precio','col_2':unicode(articulo.validez_precio)})
    data_table.append({'col_0':14, 'col_1':'cantidad_disponible','col_2':unicode(articulo.cantidad_disponible)})
    data_table.append({'col_0':15, 'col_1':'estado','col_2':unicode(articulo.estado)})
    data_table.append({'col_0':16, 'col_1':'estado_mensaje','col_2':unicode(articulo.estado_mensaje)})

    respuesta['columnas'] = columnas
    respuesta['data'] = data_table
    return JsonResponse(respuesta)

def lista_promociones_view(request):
    context = {}
    return render(request,JumboConfig.name+'/lista_promociones.html',context)

def lista_promociones_json(request):
    datos = json.loads(request.POST.get('datos'))
    respuesta = {
        'paginacion':None,
        'data':None,
        'columnas':None,
        'status':None,
        'mensaje':None,#[{type:'error|success|'<- segun swal,text:'' }]
    }
    promociones = ManagerArticuloJumbo.obtenerPromocionesJumbo().order_by('id')
    elementos_por_pagina = 20
    if 'elementos_por_pagina' in datos:
        elementos_por_pagina = int(datos['elementos_por_pagina'])
    numero_pagina_actual = 1
    if 'pagina' in datos:
        numero_pagina_actual = int(datos['pagina'])
    if 'nombre' in datos:
        if datos['nombre']:
            promociones = promociones.filter(nombre__icontains=datos['nombre'])
    if 'estado' in datos:
        if datos['estado']:
            promociones = promociones.filter(estado__icontains=datos['estado'])
    if 'promocion_id' in datos:
        if datos['promocion_id']:
            promociones = promociones.filter(promocion_id__icontains=datos['promocion_id'])

    elementos_pagina, paginacion = utils.paginacion_comun (promociones, elementos_por_pagina=elementos_por_pagina, pagina=numero_pagina_actual)
    columnas = []
    columnas.append({'title':'ID Interna', 'data':'id'});
    columnas.append({'title':'Promoción ID', 'data':'promocion_id'});
    columnas.append({'title':'Nombre promoción', 'data':'nombre_promocion'});
    columnas.append({'title':'Inicio', 'data':'fecha_inicio'});
    columnas.append({'title':'Fin', 'data':'fecha_final'});
    columnas.append({'title':'Días disponible', 'data':'dias_disponible'});
    columnas.append({'title':'Estado', 'data':'estado'});
    columnas.append({'title':'Habilitada', 'data':'habilitada'});
    columnas.append({'title':'', 'data':'ver'});
    data_table = []
    for elemento in elementos_pagina:
        aux = {}
        aux['id'] = unicode(elemento.id)
        aux['promocion_id'] = unicode(elemento.promocion_id)
        aux['nombre_promocion'] = unicode(elemento.nombre)
        aux['fecha_inicio'] = unicode(elemento.fecha_inicio)
        aux['fecha_final'] = unicode(elemento.fecha_final)
        aux['dias_disponible'] = unicode(elemento.dias_disponible)
        aux['estado'] = unicode(elemento.estado)
        aux['habilitada'] = unicode(elemento.habilitada)
        aux['ver'] = '<button name="mostrar_elemento" elemento_id="'+unicode(elemento.id)+'">Ver</button>'
        # aux['id'] = unicode(elemento.id)
        # aux['producto_id'] = unicode(elemento.producto_id)
        # aux['nombre'] = elemento.nombre
        # aux['marca'] = elemento.marca
        # aux['precio'] = elemento.precio
        # aux['precio_sin_descuento'] = elemento.precio_sin_descuento
        # aux['imagen'] = '<img src="'+elemento.url_imagen+'" style="width: 100px;height: 100px;">'
        # aux['link'] = '<a href="'+elemento.url_producto+'" target="_blank">LINK</a>'
        data_table.append(aux)
    respuesta['paginacion']=paginacion
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


def ver_promocion_json(request):
    datos = json.loads(request.POST.get('datos'))
    respuesta = {
        'data':[],
        'columnas':[],
        'status':'success',
        'mensaje':None,#[{type:'error|success|'<- segun swal,text:'' }]
    }
    articulo = None
    if 'elemento_id' in datos:
        if datos['elemento_id']:
            promocion = ManagerArticuloJumbo.obtenerPromocionJumbo(int(datos['elemento_id']))
    if promocion is None:
        respuesta['mensaje'] = [{'type':'error', 'text':'No existe la Promocion' }]
        respuesta['status'] = 'error'
        return JsonResponse(respuesta)
    columnas = []
    columnas.append({'title':'°', 'data':'col_0'});
    columnas.append({'title':'Característica', 'data':'col_1'});
    columnas.append({'title':'Detalle', 'data':'col_2'});

    data_table = []
    data_table.append({'col_0':0, 'col_1':'ID','col_2':unicode(promocion.id)})
    data_table.append({'col_0':1, 'col_1':'Promoción ID','col_2':unicode(promocion.promocion_id)})
    data_table.append({'col_0':2, 'col_1':'Nombre','col_2':unicode(promocion.nombre)})
    data_table.append({'col_0':3, 'col_1':'Grupo','col_2':unicode(promocion.grupo)})
    data_table.append({'col_0':4, 'col_1':'Tipo','col_2':unicode(promocion.tipo)})
    data_table.append({'col_0':5, 'col_1':'Tipo de descuento','col_2':unicode(promocion.tipo_descuento)})
    data_table.append({'col_0':6, 'col_1':'Tipo de promoción','col_2':unicode(promocion.tipo_promocion)})
    data_table.append({'col_0':7, 'col_1':'Valor','col_2':unicode(promocion.valor)})
    data_table.append({'col_0':8, 'col_1':'Fecha de inicio','col_2':unicode(promocion.fecha_inicio)})
    data_table.append({'col_0':9, 'col_1':'Fecha final','col_2':unicode(promocion.fecha_final)})
    data_table.append({'col_0':10, 'col_1':'Dias disponibles','col_2':unicode(promocion.dias_disponible)})
    data_table.append({'col_0':11, 'col_1':'Cantidad','col_2':unicode(promocion.cantidad)})
    data_table.append({'col_0':12, 'col_1':'Cantidad afectada','col_2':unicode(promocion.cantidad_afectada)})
    data_table.append({'col_0':13, 'col_1':'Estado','col_2':unicode(promocion.estado)})
    data_table.append({'col_0':14, 'col_1':'Estado mensaje','col_2':unicode(promocion.estado_mensaje)})

    respuesta['columnas'] = columnas
    respuesta['data'] = data_table
    return JsonResponse(respuesta)
