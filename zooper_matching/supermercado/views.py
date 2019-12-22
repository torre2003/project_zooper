# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from framework_supermercado import ManagerLogSupermercado, ManagerConfiguracionSupermercado
from framework_actualizacion_supermercado import ManagerSupermercados
from apps import SupermercadoConfig
from common import utils


def configuraciones_view(request):
    context = {}
    return render(request,SupermercadoConfig.name+'/configuraciones.html',context)


def configuraciones_json(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Tipo', 'data':'tipo'});
    columnas.append({'title':'Valor', 'data':'valor'});
    data_table = []
    configuracionessupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado()
    for configuracionsupermercado in configuracionessupermercado:
        aux = {}
        aux['id'] = unicode(configuracionsupermercado.id)
        aux['nombre'] = configuracionsupermercado.nombre
        aux['tipo'] = configuracionsupermercado.tipo
        aux['valor'] = configuracionsupermercado.valor
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


def logsupermercado_view(request):
    context = {}
    return render(request,SupermercadoConfig.name+'/logsupermercado.html',context)


def logsupermercado_json(request):
    print request.GET
    print request.POST
    print request.POST.get('datos')
    datos = {}
    if request.POST.get('datos') is not None:
        datos = json.loads(request.POST.get('datos'))
    respuesta = {
        'paginacion':None,
        'data':None,
        'columnas':None,
        'status':None,
        'mensaje':None,#[{type:'error|success|'<- segun swal,text:'' }]
    }
    items_query = ManagerLogSupermercado.obtenerLogsSupermercado().order_by('id')

    if 'grupo' in datos:
        if datos['grupo']:
            items_query = items_query.filter(grupo__icontains=datos['grupo'])
    if 'tipo' in datos:
        if datos['tipo']:
            items_query = items_query.filter(tipo__icontains=datos['tipo'])
    if 'status' in datos:
        if datos['status']:
            items_query = items_query.filter(status__icontains=datos['status'])

    elementos_por_pagina = 20
    if 'elementos_por_pagina' in datos:
        elementos_por_pagina = int(datos['elementos_por_pagina'])
    numero_pagina_actual = 1
    if 'pagina' in datos:
        numero_pagina_actual = int(datos['pagina'])
    elementos_pagina, paginacion = utils.paginacion_comun (items_query, elementos_por_pagina=elementos_por_pagina, pagina=numero_pagina_actual)
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Fecha', 'data':'fecha'});
    # columnas.append({'title':'User', 'data':'user'});
    columnas.append({'title':'Grupo', 'data':'grupo'});
    columnas.append({'title':'Tipo', 'data':'tipo'});
    columnas.append({'title':'Status', 'data':'status'});
    columnas.append({'title':'Info', 'data':'info'});
    data_table = []
    # configuracionessupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado()
    # for configuracionsupermercado in configuracionessupermercado:
    for elemento in elementos_pagina:
        aux = {}
        aux['id'] = elemento.id
        aux['fecha'] = elemento.fecha
        # aux['user'] = 'user'
        aux['grupo'] = elemento.grupo
        aux['tipo'] = elemento.tipo
        aux['status'] = elemento.status
        info = ''
        for key in elemento.info:
            info += '<p> '+unicode(key)+' -> '+unicode(elemento.info[key])+'</p>'
        aux['info'] = info
        data_table.append(aux)
    respuesta['paginacion']=paginacion
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)

def acciones_view(request):
    context = {}
    return render(request,SupermercadoConfig.name+'/acciones.html',context)
