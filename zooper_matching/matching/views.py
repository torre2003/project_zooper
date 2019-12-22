# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .apps import MatchingConfig
from producto.framework_zooper import ManagerProductoZooper
from producto.framework_jumbo import ManagerProductoJumbo
from producto.framework_telemercado import ManagerProductoTelemercado
from producto.framework_tottus import ManagerProductoTottus
from producto.framework_lider import ManagerProductoLider


def index_view(request):
    context = {}
    return render(request,MatchingConfig.name+'/index.html',context)


def matching_productos_supermercado_especifico_view(request):
    context = {}
    return render(request,MatchingConfig.name+'/matching_productos_supermercado_especifico.html',context)


def consulta_producto_supermercado_especifico_json(request):
    supermercado = request.POST.get('supermercado')
    manager = None
    if supermercado == 'jumbo':
        manager = ManagerProductoJumbo()

    respuesta = {}
    columnas = []
    columnas.append({'title':'Nombre producto', 'data':'nombre'});
    columnas.append({'title':'Marca', 'data':'marca'});
    columnas.append({'title':'Medida', 'data':'medida'});
    columnas.append({'title':'Precio', 'data':'precio'});
    columnas.append({'title':'Precio x unidad de medida', 'data':'precio_unidad_medida'});
    columnas.append({'title':'URL', 'data':'url'});
    respuesta['status'] = 'success'
    respuesta['mensaje'] = {}
    respuesta['columnas'] = columnas
    respuesta['info_producto'] = {
        'titulo': 'Sin producto',
        'info':[],
    }
    if manager == None:
        respuesta['data'] = []
        respuesta['status'] = 'error'
        respuesta['mensaje'] = {'text':'No se ha seleccionado un supermercado valido','type':'error'}
        return JsonResponse(respuesta)
    producto = manager.siguienteProducto()

    if supermercado == 'jumbo':
        respuesta['info_producto'] = {
            'titulo': producto[0].titulo,
            'info': [
                producto[0].marca,
                '<a href="'+producto[0].url+'" >'+producto[0].url+'</a>',
                '<a href="'+producto[0].image_urls+'" >'+producto[0].image_urls+'</a>',
            ]
        }
    ## Siguiente producto deberia un producto zooper, no del supermercado especifico
    ## DESDE producto zooper A Jumbo 
    data_table = []
    manager.coincidencias_zooper(producto_zooper_id=4)
    productos_zooper = ManagerProductoZooper().obtenerProductos(limit=5)
    for producto in productos_zooper:
        aux = {}
        aux['nombre'] = producto.nombre_producto
        aux['marca'] = producto.marca
        aux['medida'] = producto.medida
        aux['precio'] = producto.precio
        aux['precio_unidad_medida'] = producto.precio_unidad_medida
        aux['url'] = '<a href="'+producto.url+'" target="_blank">LINK</a>'
        data_table.append(aux)
    respuesta['data']=data_table
    return JsonResponse(respuesta)


def matching_productos_supermercado_zooper_view(request):
    context = {}
    return render(request,MatchingConfig.name+'/matching_productos_supermercado_zooper.html',context)


def consulta_producto_supermercado_zooper_json(request):
    producto_zooper_id = request.POST.get('zooper_id')
    manager_supermercados = []
    manager_supermercados.append(ManagerProductoJumbo())
    manager_supermercados.append(ManagerProductoTelemercado())
    manager_supermercados.append(ManagerProductoTottus())
    manager_supermercados.append(ManagerProductoLider())

    productozooper = ManagerProductoZooper().obtenerProducto(producto_zooper_id)
    if productozooper is None:
        return JsonResponse({
            'state':'error',
            'messages':[{'text':'No existe el producto zooper','type':'error'}],
        })

    nombre_tabla = ManagerProductoZooper().clase
    titulo = ManagerProductoZooper().titulo
    columnas = []
    columnas.append({'title':'Atributo', 'data':'col_1'});
    columnas.append({'title':'Valor', 'data':'col_2'});
    datos = []
    datos.append({'col_1':'Nombre producto', 'col_2':productozooper.nombre_producto});
    datos.append({'col_1':'Marca', 'col_2':productozooper.marca});
    datos.append({'col_1':'Medida', 'col_2':productozooper.medida});
    datos.append({'col_1':'Precio', 'col_2':productozooper.precio});
    datos.append({'col_1':'Precio x unidad de medida', 'col_2':productozooper.precio_unidad_medida});
    datos.append({'col_1':'URL', 'col_2':'<a href="'+productozooper.url+'" target="_blank">LINK</a>'});

    aux_codigo_imagen = productozooper.url.split('/')
    codigo_imagen = aux_codigo_imagen[len(aux_codigo_imagen)-1]
    datos.append({'col_1':'IMAGEN', 'col_2':'<a href="https://images.lider.cl/wmtcl?source=url[file:/productos/'+codigo_imagen+'a.jpg]&viewport=color[white],width[1000],height[1000],seed[1508522692],vsize[600],x[0],y[0]&sink" target="_blank">LINK IMAGEN</a> <img src="https://images.lider.cl/wmtcl?source=url[file:/productos/'+codigo_imagen+'a.jpg]&viewport=color[white],width[1000],height[1000],seed[1508522692],vsize[600],x[0],y[0]&sink" style="width: 400px;height: 400px;" >'});
    tabla_zooper = {
        'nombre_tabla':nombre_tabla,
        'titulo':titulo,
        'columnas':columnas,
        'datos':datos,
    }

    tablas_coincidencias = []
    for manager in manager_supermercados:
        coincidencias = manager.coincidenciasZooper(productozooper.id)
        respuesta = {}
        nombre_tabla = unicode(type(manager))
        titulo = unicode(type(manager))
        keys = []
        if len(coincidencias) > 0:
            for key in coincidencias[0]:
                keys.append(key);
        columnas = []
        if manager.clase == 'ProductoJumbo':
            columnas=[
                {u'data': u'opcion', u'title': u'Opcion', u'className': "align-center"},
                {u'data': u'puntaje', u'title': u'Puntaje'},
                {u'data': 'titulo', u'title': 'Titulo'},
                {u'data': 'marca', u'title': 'Marca'},
                {u'data': 'precio', u'title': 'Precio'}, 
                {u'data': 'url', u'title': 'URL producto'},
                {u'data': 'image_urls', u'title': 'URL imagen'},
                {u'data': 'id', u'title': 'Id producto'},
                {u'data': 'codigo', u'title': 'Código Supermercado'},
                {u'data': 'productozooper_id', u'title': 'Zooper Id'},
            ]
        elif manager.clase == 'ProductoTelemercado':
            columnas=[
                {u'data': u'opcion', u'title': u'Opcion', u'className': "align-center"},
                {u'data': u'puntaje', u'title': u'Puntaje'},
                {u'data': 'titulo', u'title': 'Titulo'},
                {u'data': 'detalle', u'title': 'Detalle'},
                {u'data': 'url_imagen', u'title': 'URL imagen'},
                {u'data': 'precio', u'title': 'Precio'},
                {u'data': 'id', u'title': 'Id producto'},
                {u'data': 'codigo', u'title': 'Código Supermercado'},
                {u'data': 'productozooper_id', u'title': 'Zooper Id'},
            ]
        elif manager.clase == 'ProductoTottus':
            columnas=[
                {u'data': u'opcion', u'title': u'Opcion', u'className': "align-center"},
                {u'data': 'marca', u'title': 'Marca'},
                {u'data': 'nombre', u'title': 'Nombre'},
                {u'data': 'medida', u'title': 'medida'},
                {u'data': 'url_imagen', u'title': 'URL imagen'},
                {u'data': u'puntaje', u'title': u'Puntaje'},
                {u'data': 'precio', u'title': 'Precio'},
                {u'data': 'link', u'title': 'URL producto'},
                {u'data': 'id', u'title': 'Id producto'},
                {u'data': 'codigo', u'title': 'Código Supermercado'},
                {u'data': 'productozooper_id', u'title': 'Zooper Id'},
            ]
        elif manager.clase == 'ProductoLider':
            columnas=[
                {u'data': u'opcion', u'title': u'Opcion', u'className': "align-center"},
                {u'data': 'titulo', u'title': 'Titulo'},
                {u'data': 'sub_titulo', u'title': 'Sub Titulo'},
                {u'data': u'caracteristica', u'title': u'Caracteristicas'},
                {u'data': 'url_imagen', u'title': 'URL imagen'},
                {u'data': u'puntaje', u'title': u'Puntaje'},
                {u'data': 'precio', u'title': 'Precio'},
                {u'data': u'precio_unidad_medida', u'title': u'Precio x unidad de medida'},
                {u'data': u'url', u'title': 'URL PRODUCTO'},
                {u'data': 'id', u'title': 'Id producto'},
                {u'data': 'codigo', u'title': 'Código Supermercado'},
                {u'data': 'productozooper_id', u'title': 'Zooper Id'},
            ]
        else:
            for key in keys:
                columnas.append({'title':key, 'data':key})
        print columnas
        datos = []
        for coincidencia in coincidencias:
            aux = {}
            for key in keys:
                aux[key]=coincidencia[key]
            if manager.clase == 'ProductoJumbo':
                aux['image_urls'] = '<a href="'+aux['image_urls']+'" target="_blank">LINK IMAGEN</a> <img src="'+aux['image_urls']+'" style="width: 400px;height: 400px;" >'
                aux['url'] = '<a href="'+aux['url']+'" target="_blank">LINK PRODUCTO</a>'
            if manager.clase == 'ProductoTelemercado':
                aux['url_imagen'] = '<a href="https://supermercado.telemercados.cl/'+aux['url_imagen']+'" target="_blank">LINK IMAGEN</a> <img src="https://supermercado.telemercados.cl/'+ aux['url_imagen'].replace('../','' )+'" style="width: 400px;height: 400px;" >'
                #aux['url'] = '<a href="'+aux['url']+'" target="_blank">LINK PRODUCTO</a>'
            if manager.clase == 'ProductoTottus':
                aux['url_imagen'] = '<a href="http://s7d2.scene7.com/is/image/Tottus/'+aux['codigo']+'?$S7Product$&wid=458&hei=458&op_sharpen=0" target="_blank">LINK IMAGEN</a> <img src="http://s7d2.scene7.com/is/image/Tottus/'+aux['codigo']+'?$S7Product$&wid=458&hei=458&op_sharpen=0" style="width: 400px;height: 400px;" >'
            if manager.clase == 'ProductoLider':
                aux_codigo_imagen = aux['url'].split('/')
                codigo_imagen = aux_codigo_imagen[len(aux_codigo_imagen)-1]
                aux['url_imagen'] = '<a href="https://images.lider.cl/wmtcl?source=url[file:/productos/'+codigo_imagen+'a.jpg]&viewport=color[white],width[1000],height[1000],seed[1508522692],vsize[600],x[0],y[0]&sink" target="_blank">LINK IMAGEN</a> <img src="https://images.lider.cl/wmtcl?source=url[file:/productos/'+codigo_imagen+'a.jpg]&viewport=color[white],width[1000],height[1000],seed[1508522692],vsize[600],x[0],y[0]&sink" style="width: 400px;height: 400px;" >'
            selected = ''
            if aux['productozooper_id'] == productozooper.id:
                print aux
                print 'CHECKED ',manager.clase
                selected = 'checked="checked"'
            aux['opcion'] = '<input name="'+manager.clase+'" id="'+manager.clase+'_'+unicode(aux['id'])+'" class="with-gap" type="radio" value="'+unicode(aux['id'])+'"   '+selected+'>'+'<label for="'+manager.clase+'_'+unicode(aux['id'])+'"></label>'
            datos.append(aux)
        tablas_coincidencias.append({
            'nombre_tabla':manager.clase,
            'titulo':manager.titulo,
            'columnas':columnas,
            'datos':datos,
        })

    respuesta['state'] = 'success'
    respuesta['messages'] = []
    respuesta['tabla_zooper'] = tabla_zooper
    respuesta['tablas_coincidencias'] = tablas_coincidencias
    return JsonResponse(respuesta)


    """
        {
            producto_zooper_id: 122,
            supermercados:{
                ProductoJumbo: 123
                ProductoTelemercado : 1231
                ProductoTottus : None
                ProductoLider : 1233
            }
        }
    """

def vincular_producto_supermercado_zooper_json(request):
    datos = json.loads(request.POST.get('datos'))
    print 'Vincular producto'
    print datos
    manager_zooper = ManagerProductoZooper()
    manager_supermercados = {
        'ProductoJumbo': ManagerProductoJumbo(),
        'ProductoTelemercado': ManagerProductoTelemercado(),
        'ProductoTottus': ManagerProductoTottus(),
        'ProductoLider': ManagerProductoLider(),
    }
    productozooper = manager_zooper.obtenerProducto(datos['productozooper_id'])
    if productozooper is None:
        return JsonResponse({
            'state':'error',
            'messages':[{'text':'No existe el producto zooper','type':'error'}],
        })
    supermercados = datos['supermercados']
    for key_manager in manager_supermercados:
        if manager_supermercados[key_manager].clase in supermercados:
            if supermercados[key_manager] != '':
                manager_supermercados[key_manager].vincularProducto(
                    producto_id=supermercados[key_manager],
                    productozooper_id=productozooper.id, 
                )
            else:
                manager_supermercados[key_manager].desvincularProducto(
                    productozooper_id=productozooper.id, 
                )
    return JsonResponse({
        'state':'success',
        'messages':[],
    })