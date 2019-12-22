# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .apps import ProductoConfig

from framework_producto import ManagerProducto
from producto.framework_zooper import ManagerProductoZooper
from producto.framework_jumbo import ManagerProductoJumbo
from producto.framework_telemercado import ManagerProductoTelemercado
from producto.framework_tottus import ManagerProductoTottus
from producto.framework_lider import ManagerProductoLider


def obtener_productos_a_actualizar_json(request):
    manager = ManagerProducto()
    respuesta = manager.obtenerProductosAActualizar()
    return JsonResponse(respuesta, safe=False)


def actualizacion_registro_producto_json(request):
    print request.GET
    return JsonResponse({'status':'success'}, safe=False)


def obtener_productos_custom_json(request):
    respuesta = []
    try:
        supermercado = request.GET.get('supermercado')
        opcion = request.GET.get('opcion')
    except Exception, e:
        print 'error de parametros'
    if supermercado == 'telemercado':
        if opcion == 'urls_update':
            productos = ManagerProductoTelemercado().obtenerProductos().filter(estado='NO_ACTUALIZADO')[:5000]
            print productos
            for producto in productos:
                producto.estado = 'PENDIENTE_ACTUALIZACION'
                producto.save()
                respuesta.append ({
                    'supermercado':ManagerProductoTelemercado().supermercado,
                    'productosupermercado_id':producto.id,
                    'url':ManagerProductoTelemercado().obtenerLinkProducto(producto)
                })
    return JsonResponse(respuesta, safe=False)


def actualizacion_producto_custom_json(request):
    respuesta = []
    params = {}

    manager = {
        'zooper':ManagerProductoZooper(),
        'jumbo':ManagerProductoJumbo(),
        'telemercado':ManagerProductoTelemercado(),
        'tottus':ManagerProductoTottus(),
        'lider':ManagerProductoLider(),
    }

    try:

        params['cod_supermercado'] = request.GET.get('cod_supermercado')
        params['supermercado'] = request.GET.get('supermercado')
        params['status_actualizacion'] = request.GET.get('status_actualizacion')
        extra_params = request.GET.get('params')
        params['params'] = extra_params.split(',')
        productosupermercado = manager[params['supermercado']].obtenerProducto(int(params['cod_supermercado']))
        productosupermercado.estado = params['status_actualizacion']
        for param in params['params']:
            if param == 'url':
                productosupermercado.url = request.GET.get('url')
        productosupermercado.save()
        print productosupermercado.id,' - ',productosupermercado.estado,' - ',productosupermercado.url
    except Exception, e:
        print 'error en parametros'

    return JsonResponse(respuesta, safe=False)