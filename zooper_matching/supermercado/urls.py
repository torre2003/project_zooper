# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from . import views
from . import views_interaccion_publica
from apps import SupermercadoConfig

app_name = SupermercadoConfig.name
urlpatterns = [
    url(r'^jumbo/', include('supermercado.jumbo.urls')),
    
    url(r'^acciones$', views.acciones_view, name='acciones'),

    url(r'^configuraciones$', views.configuraciones_view, name='configuraciones'),
    url(r'^configuraciones_json$', views.configuraciones_json, name='configuraciones-json'),

    url(r'^logsupermercado$', views.logsupermercado_view, name='logsupermercado'),
    url(r'^logsupermercado_json$', views.logsupermercado_json, name='logsupermercado-json'),

    url(r'^obtener_articulos_supermercados_json$', views_interaccion_publica.obtener_articulos_supermercados_json, name='obtener-articulos-supermercados-json'),
    url(r'^ingresar_articulos_supermercados_json$', views_interaccion_publica.ingresar_articulos_supermercados_json, name='ingresar-articulos-supermercados-json'),
    # url(r'^configuraciones/$', views.index_view, name='configuraciones'),
    # url(r'^productos_con_codigo_zooper/$', views.productos_con_codigo_zooper_view, name='productos-con-codigo-zooper'),
    # url(r'^productos_con_codigo_zooper_json/$', views.productos_con_codigo_zooper_json, name='productos-con-codigo-zooper-json')
]