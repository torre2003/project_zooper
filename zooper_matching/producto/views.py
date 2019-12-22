# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .apps import ProductoConfig

from producto.framework_zooper import ManagerProductoZooper
from producto.framework_jumbo import ManagerProductoJumbo
from producto.framework_telemercado import ManagerProductoTelemercado
from producto.framework_tottus import ManagerProductoTottus
from producto.framework_lider import ManagerProductoLider


def index_view(request):
    context = {}
    return render(request,ProductoConfig.name+'/index.html',context)


def productos_con_codigo_zooper_view(request):
    context = {}
    return render(request,ProductoConfig.name+'/productos_con_codigo_zooper.html',context)


def productos_con_codigo_zooper_json(request):

    productos_zooper = {}

    manager_zooper = ManagerProductoZooper()
    manager_supermercados = []
    manager_supermercados.append(ManagerProductoJumbo())
    manager_supermercados.append(ManagerProductoTelemercado())
    manager_supermercados.append(ManagerProductoTottus())
    manager_supermercados.append(ManagerProductoLider())

    for manager in manager_supermercados:
        productos = manager.obtenerProductos()
        productos.filter(productozooper__isnull=False)
        for producto in productos:
            if not producto.productozooper_id in productos_zooper:
                productos_zooper[producto.productozooper_id] = {}
            productos_zooper[producto.productozooper_id][manager.clase] = producto.id



    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre producto', 'data':'nombre'});
    columnas.append({'title':'Marca', 'data':'marca'});
    #columnas.append({'title':'Medida', 'data':'medida'});
    #columnas.append({'title':'Precio', 'data':'precio'});
    #columnas.append({'title':'Precio x unidad de medida', 'data':'precio_unidad_medida'});
    columnas.append({'title':'URL', 'data':'url'});
    columnas.append({'title':'Jumbo', 'data':'ProductoJumbo'});
    columnas.append({'title':'Lider', 'data':'ProductoLider'});
    columnas.append({'title':'Telemercado', 'data':'ProductoTelemercado'});
    columnas.append({'title':'Tottus', 'data':'ProductoTottus'});
    respuesta['status'] = 'success'
    respuesta['mensaje'] = {}
    respuesta['columnas'] = columnas
    
    respuesta['info_producto'] = {
        'titulo': 'Sin producto',
        'info':[],
    }

    data_table = []
    for productozooper_id in productos_zooper:
        if productozooper_id is not None and len(productos_zooper[productozooper_id]) > 1:
            productozooper = manager_zooper.obtenerProducto(productozooper_id)
            aux = {}
            aux['id'] = productozooper.id
            aux['nombre'] = productozooper.nombre_producto
            aux['marca'] = productozooper.marca
            #aux['medida'] = productozooper.medida
            #aux['precio'] = 'productozooper.precio'
            #aux['precio_unidad_medida'] = 'productozooper.precio_unidad_medida'
            aux['url'] = '<a href="" target="_blank">LINK</a>'
            aux['ProductoJumbo'] = '---'
            aux['ProductoLider'] = '---'
            aux['ProductoTelemercado'] = '---'
            aux['ProductoTottus'] = '---'
            for producto_asociado in productos_zooper[productozooper_id]:
                aux[producto_asociado] = productos_zooper[productozooper_id][producto_asociado]
            data_table.append(aux)

    respuesta['data']=data_table
    return JsonResponse(respuesta)
