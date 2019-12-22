# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib3
import urllib2
import urllib
from urllib import urlencode
import os
# from urllib .parse import urlencode

from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.context_processors import csrf

from apps import CommonConfig

from producto.importaciones.lider import importar_lider
from producto.importaciones.jumbo import importar_jumbo
from producto.importaciones.telemercado import importar_telemercado
from producto.importaciones.tottus import importar_tottus

from producto.models import ProductoZooper, ProductoLider, ProductoJumbo, ProductoTelemercado, ProductoTottus

from supermercado.lider.framework_lider import ManagerArticuloLider

from producto.framework_producto import ManagerProducto
from producto.framework_jumbo import ManagerProductoJumbo
from producto.framework_lider import ManagerProductoLider
from producto.framework_telemercado import ManagerProductoTelemercado
from producto.framework_tottus import ManagerProductoTottus
from producto.framework_zooper import ManagerProductoZooper

from supermercado.jumbo.framework_jumbo import ManagerArticuloJumbo
from supermercado.jumbo.framework_actualizacion_jumbo import ManagerActualizacionJumbo
from supermercado.lider.framework_actualizacion_lider import ManagerActualizacionLider
from supermercado.framework_supermercado import ManagerConfiguracionSupermercado

from common import utils_bdd

def view_test(request):
    context = {}
    return render(request, CommonConfig.name+'/test.html', context)



def json_test_01(request):
    print '*'*10,'   Test-01    ','*'*10
    if False:
        p = ManagerConfiguracionSupermercado.crearConfiguracionSupermercado(
            nombre='lider_limite_busqueda', 
            valor=50,
            tipo="NUMERO"
        )
        p = ManagerConfiguracionSupermercado.crearConfiguracionSupermercado(
            nombre='lider_maximo_intentos_busqueda', 
            valor=5,
            tipo="NUMERO"
        )
        # p = ManagerConfiguracionSupermercado.crearConfiguracionSupermercado(
        #     nombre='jumbo_url_base_query', 
        #     valor='&fq=productId%3A',
        #     tipo="TEXTO"
        # )
    return JsonResponse({})



def json_test_02(request):
    print '*'*10,'   Test-02    ','*'*10
    print 'Producto Jumbo'
    # url = 'https://www.lider.cl/supermercado/product/Vital-Agua-Mineral-Con-Gas/4569'
    print ManagerActualizacionLider.obtenerUrlsInfoBusquedaArticulosEnProceso()

    return JsonResponse({})


def json_test_03(request):
    print '*'*10,'   Test-03    ','*'*10
    print ManagerActualizacionJumbo.generarURLArticulos(
        identificadores=[u'57561', u'57666', u'57735', u'57790', u'57818', u'57851', u'57876', u'57887', u'57898', u'57908', u'57936', u'57949', u'57958', u'57964', u'57968', u'57972', u'57980', u'57985', u'58000', u'58004', u'58008', u'58012', u'58018',u'58024', u'58028', u'58033', u'58038', u'58044', u'58047', u'58049', u'58051', u'58053', u'58055', u'58057', u'58059', u'58061', u'58063', u'58065', u'58067', u'58070', u'58072', u'58075', u'58077', u'58079', u'58081', u'58083',u'58085', u'58087', u'58089', u'58091']
            ,url_unica=True
        )
    print '*'*10,'   Test-03    ','*'*10
    return JsonResponse({})



def json_test_04(request):
    print '*'*10,'   Test-04    ','*'*10
    #importar_tottus()
    a = ManagerActualizacionJumbo.obtenerURLArticulosAActualizar(url_unica=False, limit=50, estados=['PENDIENTE_ACTUALIZACION'])
    print a
    print '*'*10,'   Test-04    ','*'*10
    return JsonResponse({})



def json_test_05(request):
    print '*'*10,'   Test-05    ','*'*10
    http = urllib3.PoolManager()
    urls = []
    # urls.append(r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A101&fq=productId%3A102&fq=productId%3A103&fq=productId%3A104&fq=productId%3A105&fq=productId%3A106&fq=productId%3A107&fq=productId%3A108&fq=productId%3A109&fq=productId%3A110&fq=productId%3A111&fq=productId%3A112&fq=productId%3A113&fq=productId%3A114&fq=productId%3A115&fq=productId%3A116&fq=productId%3A117&fq=productId%3A118&fq=productId%3A119&fq=productId%3A120&fq=productId%3A121&fq=productId%3A122&fq=productId%3A123&fq=productId%3A124&fq=productId%3A125&fq=productId%3A126&fq=productId%3A127&fq=productId%3A128&fq=productId%3A129&fq=productId%3A130&fq=productId%3A131&fq=productId%3A132&fq=productId%3A133&fq=productId%3A134&fq=productId%3A135&fq=productId%3A136&fq=productId%3A137&fq=productId%3A138&fq=productId%3A139&fq=productId%3A140&fq=productId%3A141&fq=productId%3A142&fq=productId%3A143&fq=productId%3A144&fq=productId%3A145&fq=productId%3A146&fq=productId%3A147&fq=productId%3A148&fq=productId%3A149&fq=productId%3A150"]}')
    # urls.append(r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A151&fq=productId%3A152&fq=productId%3A153&fq=productId%3A154&fq=productId%3A155&fq=productId%3A156&fq=productId%3A157&fq=productId%3A158&fq=productId%3A159&fq=productId%3A160&fq=productId%3A161&fq=productId%3A162&fq=productId%3A163&fq=productId%3A164&fq=productId%3A165&fq=productId%3A166&fq=productId%3A167&fq=productId%3A168&fq=productId%3A169&fq=productId%3A170&fq=productId%3A171&fq=productId%3A172&fq=productId%3A173&fq=productId%3A174&fq=productId%3A175&fq=productId%3A176&fq=productId%3A177&fq=productId%3A178&fq=productId%3A179&fq=productId%3A180&fq=productId%3A181&fq=productId%3A182&fq=productId%3A183&fq=productId%3A184&fq=productId%3A185&fq=productId%3A186&fq=productId%3A187&fq=productId%3A188&fq=productId%3A189&fq=productId%3A190&fq=productId%3A191&fq=productId%3A192&fq=productId%3A193&fq=productId%3A194&fq=productId%3A195&fq=productId%3A196&fq=productId%3A197&fq=productId%3A198&fq=productId%3A199&fq=productId%3A200"]}')
    urls.append(r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A68087"]}')
    for url in urls:
        info = json.loads(url)
        for supermercado in info:
            for url_supermercado in info[supermercado]:
                r = http.request('GET', url_supermercado)
                if supermercado == 'jumbo':
                    # load = json.loads(r.data.decode('utf-8'))
                    print 'vvv'*20
                    print r.data
                    print '^^^^^^^^^^^^^^'*20
                    ManagerActualizacionJumbo.ingresarArticuloJumboLote(r.data)
    print '*'*10,'   Test-05    ','*'*10
    return JsonResponse({})



def json_test_06(request):
    print '*'*10,'   Test-06    ','*'*10
    print ' Buscando articulos'
    # json_jumbo_0 = r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?", "https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A101&fq=productId%3A102&fq=productId%3A103&fq=productId%3A104&fq=productId%3A105&fq=productId%3A106&fq=productId%3A107&fq=productId%3A108&fq=productId%3A109&fq=productId%3A110&fq=productId%3A111&fq=productId%3A112&fq=productId%3A113&fq=productId%3A114&fq=productId%3A115&fq=productId%3A116&fq=productId%3A117&fq=productId%3A118&fq=productId%3A119&fq=productId%3A120&fq=productId%3A121&fq=productId%3A122&fq=productId%3A123&fq=productId%3A124&fq=productId%3A125&fq=productId%3A126&fq=productId%3A127&fq=productId%3A128&fq=productId%3A129&fq=productId%3A130&fq=productId%3A131&fq=productId%3A132&fq=productId%3A133&fq=productId%3A134&fq=productId%3A135&fq=productId%3A136&fq=productId%3A137&fq=productId%3A138&fq=productId%3A139&fq=productId%3A140&fq=productId%3A141&fq=productId%3A142&fq=productId%3A143&fq=productId%3A144&fq=productId%3A145&fq=productId%3A146&fq=productId%3A147&fq=productId%3A148&fq=productId%3A149&fq=productId%3A150"]}'
    json_jumbo_0 = r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A101&fq=productId%3A102&fq=productId%3A103&fq=productId%3A104&fq=productId%3A105&fq=productId%3A106&fq=productId%3A107&fq=productId%3A108&fq=productId%3A109&fq=productId%3A110&fq=productId%3A111&fq=productId%3A112&fq=productId%3A113&fq=productId%3A114&fq=productId%3A115&fq=productId%3A116&fq=productId%3A117&fq=productId%3A118&fq=productId%3A119&fq=productId%3A120&fq=productId%3A121&fq=productId%3A122&fq=productId%3A123&fq=productId%3A124&fq=productId%3A125&fq=productId%3A126&fq=productId%3A127&fq=productId%3A128&fq=productId%3A129&fq=productId%3A130&fq=productId%3A131&fq=productId%3A132&fq=productId%3A133&fq=productId%3A134&fq=productId%3A135&fq=productId%3A136&fq=productId%3A137&fq=productId%3A138&fq=productId%3A139&fq=productId%3A140&fq=productId%3A141&fq=productId%3A142&fq=productId%3A143&fq=productId%3A144&fq=productId%3A145&fq=productId%3A146&fq=productId%3A147&fq=productId%3A148&fq=productId%3A149&fq=productId%3A150"]}'
    json_jumbo_1 = r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A151&fq=productId%3A152&fq=productId%3A153&fq=productId%3A154&fq=productId%3A155&fq=productId%3A156&fq=productId%3A157&fq=productId%3A158&fq=productId%3A159&fq=productId%3A160&fq=productId%3A161&fq=productId%3A162&fq=productId%3A163&fq=productId%3A164&fq=productId%3A165&fq=productId%3A166&fq=productId%3A167&fq=productId%3A168&fq=productId%3A169&fq=productId%3A170&fq=productId%3A171&fq=productId%3A172&fq=productId%3A173&fq=productId%3A174&fq=productId%3A175&fq=productId%3A176&fq=productId%3A177&fq=productId%3A178&fq=productId%3A179&fq=productId%3A180&fq=productId%3A181&fq=productId%3A182&fq=productId%3A183&fq=productId%3A184&fq=productId%3A185&fq=productId%3A186&fq=productId%3A187&fq=productId%3A188&fq=productId%3A189&fq=productId%3A190&fq=productId%3A191&fq=productId%3A192&fq=productId%3A193&fq=productId%3A194&fq=productId%3A195&fq=productId%3A196&fq=productId%3A197&fq=productId%3A198&fq=productId%3A199&fq=productId%3A200"]}'
    json_jumbo_2 = r'{"jumbo": ["https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A201&fq=productId%3A202&fq=productId%3A203&fq=productId%3A204&fq=productId%3A205&fq=productId%3A206&fq=productId%3A207&fq=productId%3A208&fq=productId%3A209&fq=productId%3A210&fq=productId%3A211&fq=productId%3A212&fq=productId%3A213&fq=productId%3A214&fq=productId%3A215&fq=productId%3A216&fq=productId%3A217&fq=productId%3A218&fq=productId%3A219&fq=productId%3A220&fq=productId%3A221&fq=productId%3A222&fq=productId%3A223&fq=productId%3A224&fq=productId%3A225&fq=productId%3A226&fq=productId%3A227&fq=productId%3A228&fq=productId%3A229&fq=productId%3A230&fq=productId%3A231&fq=productId%3A232&fq=productId%3A233&fq=productId%3A234&fq=productId%3A235&fq=productId%3A236&fq=productId%3A237&fq=productId%3A238&fq=productId%3A239&fq=productId%3A240&fq=productId%3A241&fq=productId%3A242&fq=productId%3A243&fq=productId%3A244&fq=productId%3A245&fq=productId%3A246&fq=productId%3A247&fq=productId%3A248&fq=productId%3A249&fq=productId%3A250"]}'
    http = urllib3.PoolManager()
    jumbo_0 = json.loads(json_jumbo_0)

    for supermercado in jumbo_0:
        i = 0
        while i < len(jumbo_0[supermercado]) :
            print '*-*-*'*15
            print '*-*-*'*15
            print ''
            print ''
            print ''
            print jumbo_0[supermercado][i]
            print ''
            print '*-*-*'*15
            print ''
            print ''
            print ''
            r = http.request('GET', jumbo_0[supermercado][i])
            if supermercado == 'jumbo':
                print r.data
                print ''
                print '*-*-* load'*15
                print ''
                load = json.loads(r.data.decode('utf-8'))

                print load[0]
                print ''
                print '*-*-* dump'*15
                print ''
                dump = json.dumps(load[0], ensure_ascii=False)
                # dump = json.dump(load[0])
                print dump
                encoded_data = json.dumps(load[0], ensure_ascii=False).encode('utf-8')
                encoded_args = urllib.urlencode({'arg': encoded_data})
                
                print 'vv'
                # data = {'attribute': 'value'}
                encoded_data = json.dumps(load[0]).encode('utf-8')
                r_e = http.request(
                    'POST',
                    'http://127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json?csrfmiddlewaretoken='+unicode(csrf(request)['csrf_token']),
                    body=encoded_data,
                    # fields={
                    #     'csrfmiddlewaretoken':csrf(request)['csrf_token']
                    # },
                    # headers={'Content-Type': 'application/json'}
                )
                print '||'

# >>> json.loads(r.data.decode('utf-8'))['json']


                # r = http.request('POST','127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json/',
                #     fields={'data': ('example.txt', r.data.decode('utf-8'))})

                # url = '127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json/?'+encoded_args
                
                print ''
                print '*-*-*'*15
                print ''

                # r_envio = http.request('POST',url)
            i = i + 1;
            print ''
            print ''
            print ''
            print '*-*-*'*15
            print '*-*-*'*15


    
    
# >>> r.status
# >>> r = http.request('GET', 'http://httpbin.org/ip')
# >>> json.loads(r.data.decode('utf-8'))
    print '*'*10,'   Test-05    ','*'*10
    return JsonResponse({})



def json_test_07(request):
    print '*'*10,'   Test-07    ','*'*10
    print ' Código de actualización para supermercado Jumbo, este código deberia estar en la cron de ejecución '
    i = 0
    http = urllib3.PoolManager()
    while i < 1:
        i+=1
        info = None
        if True:
            r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/obtener_articulos_supermercados_json?supermercado=jumbo')
            url =  r_url.data
            print '--->'
            print url
            print '--->'
            respuesta = json.loads(url)
            if respuesta['status'] == 'success':
                info = respuesta['info']
            else:
                print '  XX'*15
                print respuesta['status']
                print respuesta['message']
                info = []
        else:
            i+=9999999
            info = ['https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A17146&fq=productId%3A17314&fq=productId%3A17364&fq=productId%3A17395&fq=productId%3A17411&fq=productId%3A17432&fq=productId%3A17446&fq=productId%3A17454&fq=productId%3A17462&fq=productId%3A17470&fq=productId%3A17478&fq=productId%3A17488&fq=productId%3A17522&fq=productId%3A17526&fq=productId%3A17530&fq=productId%3A17536&fq=productId%3A17545&fq=productId%3A17556&fq=productId%3A17561&fq=productId%3A17565&fq=productId%3A17570&fq=productId%3A17575&fq=productId%3A17579&fq=productId%3A17583&fq=productId%3A17587&fq=productId%3A17590&fq=productId%3A17592&fq=productId%3A17594&fq=productId%3A17596&fq=productId%3A17598&fq=productId%3A17600&fq=productId%3A17602&fq=productId%3A17604&fq=productId%3A17606&fq=productId%3A17615&fq=productId%3A17623&fq=productId%3A17637&fq=productId%3A17641&fq=productId%3A17655&fq=productId%3A17658&fq=productId%3A17660&fq=productId%3A17665&fq=productId%3A17667&fq=productId%3A17669&fq=productId%3A17681&fq=productId%3A17684&fq=productId%3A17686&fq=productId%3A17688&fq=productId%3A17691&fq=productId%3A17693']
        for url_supermercado in info:
            r = http.request('GET', url_supermercado)
            if r.data is not None:
                if r.data:
                    ManagerActualizacionJumbo.ingresarArticuloJumboLote(r.data)
    return JsonResponse('', safe=False)



def json_test_08(request):
    print '*'*10,'   Test-08    ','*'*10
    data = os.popen('curl "https://nuevo.jumbo.cl/jumbo/dataentities/PM/documents/Promos?_fields=value"%"2Cid" --compressed').read()
    ManagerActualizacionJumbo.ingresarPromocionJumboLote(data=data, user_id=None)
    print '*'*10,'   Test-08    ','*'*10
    return JsonResponse({})



def json_test_09(request):
    print '*'*10,'   Test-09    ','*'*10
    print '*'*10,'   Actualizaciones supermercados    ','*'*10
    opcion = request.GET.get('opcion')
    if opcion == 'producto_jumbo':
        actualizacion_producto_jumbo(request)
    if opcion == 'promocion_jumbo':
        actualizacion_promociones_jumbo(request)
        pass
    elif opcion == 'producto_lider':
        actualizacion_producto_lider(request)
    elif opcion == 'producto_telemercado':
        pass
    elif opcion == 'producto_tottus':
        pass
    print '*'*10,'   Test-09    ','*'*10
    return JsonResponse({})



def view_test_11(request):
    context = {}
    return render(request, CommonConfig.name+'/ejemplo_timeline.html', context)



def actualizacion_producto_jumbo(request):
    print '*'*10,'   actualizacion_producto_jumbo-07    ','*'*10
    print ' Código de actualización para supermercado Jumbo, este código deberia estar en la cron de ejecución '
    i = 0
    http = urllib3.PoolManager()
    while i < 1:
        i+=1
        info = None
        if True:
            r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/obtener_articulos_supermercados_json?supermercado=jumbo')
            url =  r_url.data
            print url
            respuesta = json.loads(url)
            if respuesta['status'] == 'success':
                info = respuesta['info']
            else:
                print '  XX'*15
                print respuesta['status']
                print respuesta['message']
                info = []
        else:
            i+=9999999
            info = ['https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?&fq=productId%3A17146&fq=productId%3A17314&fq=productId%3A17364&fq=productId%3A17395&fq=productId%3A17411&fq=productId%3A17432&fq=productId%3A17446&fq=productId%3A17454&fq=productId%3A17462&fq=productId%3A17470&fq=productId%3A17478&fq=productId%3A17488&fq=productId%3A17522&fq=productId%3A17526&fq=productId%3A17530&fq=productId%3A17536&fq=productId%3A17545&fq=productId%3A17556&fq=productId%3A17561&fq=productId%3A17565&fq=productId%3A17570&fq=productId%3A17575&fq=productId%3A17579&fq=productId%3A17583&fq=productId%3A17587&fq=productId%3A17590&fq=productId%3A17592&fq=productId%3A17594&fq=productId%3A17596&fq=productId%3A17598&fq=productId%3A17600&fq=productId%3A17602&fq=productId%3A17604&fq=productId%3A17606&fq=productId%3A17615&fq=productId%3A17623&fq=productId%3A17637&fq=productId%3A17641&fq=productId%3A17655&fq=productId%3A17658&fq=productId%3A17660&fq=productId%3A17665&fq=productId%3A17667&fq=productId%3A17669&fq=productId%3A17681&fq=productId%3A17684&fq=productId%3A17686&fq=productId%3A17688&fq=productId%3A17691&fq=productId%3A17693']
        for url_supermercado in info:
            r = http.request('GET', url_supermercado)
            if r.data is not None:
                if r.data:
                    ManagerActualizacionJumbo.ingresarArticuloJumboLote(r.data)
    return JsonResponse('', safe=False)


def actualizacion_promociones_jumbo(request):
    print '*'*10,'   actualizacion_promociones_jumbo    ','*'*10
    data = os.popen('curl "https://nuevo.jumbo.cl/jumbo/dataentities/PM/documents/Promos?_fields=value"%"2Cid" --compressed').read()
    ManagerActualizacionJumbo.ingresarPromocionJumboLote(data=data, user_id=None)
    print '*'*10,'   actualizacion_promociones_jumbo    ','*'*10
    return JsonResponse({})



def actualizacion_producto_lider(request):
    print '*'*10,'   actualizacion_producto_lider    ','*'*10
    print 'Test de busqueda, consulta e ingreso de datos en formato de scrapy'
    i = 0
    opcion = 'ingreso_producto'
    print opcion
    http = urllib3.PoolManager()
    if opcion == 'ingreso_busqueda':
        data = r'https://www.lider.cl/supermercado/product/Nido-Leche-Semidescremada-en-Polvo-Etapa-1-/878237'
        r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json?supermercado=lider&opcion=ingreso_busqueda&data=https://www.lider.cl/supermercado/product/Drive-Detergente-L%C3%ADquido-Perfect-Results-Recarga/660114'+data)
        r_data =  r_url.data
        print r_data
    elif opcion == 'consulta':
        r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/obtener_articulos_supermercados_json?supermercado=lider')
        r_data =  r_url.data
        print r_data
        respuesta = json.loads(r_data)
        if respuesta['status'] == 'success':
            info = respuesta['info']
        else:
            print '  XX'*15
            print respuesta['status']
            print respuesta['message']
    elif opcion == 'ingreso_producto':
        r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json?supermercado=lider&opcion=ingreso_producto&status_actualizacion=actualizado&codigo=201812782347871500&data={}&cod_supermercado=498721')
        # r_url = http.request('GET', 'http://127.0.0.1:8888/supermercado/obtener_articulos_supermercados_json?supermercado=lider')
        r_data =  r_url.data
        # from urllib import urlencode
        # import urllib2
        # def http_post(url, data):
        # data = {
        #     'name' : 'james',
        #     'age' : 'blaba',
        #     'data':data_post,
        # }
        # post = urlencode(data)
        # req = urllib2.Request(url, post)
        # response = urllib2.urlopen(req)
        
        
        # data = bytes( urllib.parse.urlencode( data ).encode() )
        # handler = urllib.request.urlopen( 'http://127.0.0.1:8888/supermercado/ingresar_articulos_supermercados_json', data );
        # print( handler.read().decode( 'utf-8' ) );
        # pass
    elif opcion == 'test_01':
        print utils_bdd.extraer_data_comunicacion_scrapy('2018125101158400936')


    return JsonResponse('', safe=False)



data_post  = r'{"caracteristica":"3 L","etiquetas_precio":[{"content":"CLP","texto":"","id":"","itemprop":"priceCurrency","class":""},{"content":"10490","texto":"$10.490","id":"","itemprop":"lowPrice","class":"price"},{"content":"","texto":"Precio x L : $3.497","id":"","itemprop":"","class":""},{"content":"","texto":"","id":"price-date-info","itemprop":"","class":"note"}],"codigo":"498721","precio_unidad_medida":"PrecioxL:$3497","etiquetas_oferta":[{"otros":null,"clase":["preciolider"],"texto":null},{"otros": null,"clase":["label-llevamas"],"texto":null},{"otros":"Ahorro:$4.990","clase":["label-llevamas_fondo"],"texto":"2 X$15.990"}],"nombre":"Detergente Líquido Perfect Results Recarga","url_producto":"https://www.lider.cl/supermercado/product/Drive-Detergente-L%C3%ADquido-Perfect-Results-Recarga/660114","url_imagen":"https://images.lider.cl/wmtcl?source=url[file:/productos/660114a.jpg","precio":"10490","marca":"Drive"}'