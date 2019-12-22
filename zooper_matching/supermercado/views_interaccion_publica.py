# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from framework_actualizacion_supermercado import ManagerSupermercados
from apps import SupermercadoConfig
from common import utils_bdd

def obtener_articulos_supermercados_json(request):
    if 'supermercado' not in request.GET:
        JsonResponse({
                'status':'error',
                'message':'No se ha especificado un supermercado.'
            })
    supermercado = request.GET.get('supermercado')
    if supermercado not in ['lider', 'jumbo', '','']:
        JsonResponse({
                'status':'error',
                'message':'Supermercado desconocido'
            })
    return JsonResponse({
        'status':'success',
        'message':'',
        'info':ManagerSupermercados.obtenerElementosAActualizar(supermercado),
    })

    #ManagerSupermercados.ingresarResultadosPeticion(supermercado, data, lote=True, user_id=None):


def ingresar_articulos_supermercados_json(request):
    print 'ingresar_articulos_supermercados_json'
    if 'supermercado' not in request.GET:
        JsonResponse({'status':'error','message':'No se ha especificado un supermercado.'})
    supermercado = request.GET.get('supermercado')
    if supermercado not in ['lider', 'jumbo', '','']:
        JsonResponse({'status':'error','message':'Supermercado desconocido'})
    if 'supermercado' not in request.GET:
        JsonResponse({'status':'error','message':'No se ha especificado un supermercado.'})
    supermercado = request.GET.get('supermercado')
    if 'opcion' not in request.GET:
        JsonResponse({'status':'error','message':'No se ha especificado una opción.'})
    opcion = request.GET.get('opcion')
    if 'data' not in request.GET:
        JsonResponse({'status':'error','message':'No se han encontrado datos'})
    data = request.GET.get('data')
    if supermercado == 'jumbo':
        pass
    elif supermercado == 'lider':
        if 'codigo' in request.GET:
            codigo = request.GET.get('codigo')
            data = utils_bdd.extraer_data_comunicacion_scrapy(codigo)
        print 'ingresar_articulos_supermercados_json - data'
        print data
        ManagerSupermercados.ingresarResultadosPeticion(supermercado=supermercado, data=data, opcion=opcion, lote=True, user_id=None)
    return JsonResponse({'status':'success'})



