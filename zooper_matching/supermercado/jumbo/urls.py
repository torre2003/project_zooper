# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from apps import JumboConfig


app_name = JumboConfig.name

urlpatterns = [
    # url(r'^$', views.index_view, name='index'),
    url(r'^lista_articulos/$', views.lista_articulos_view, name='lista-articulos'),
    url(r'^lista_articulos_json/$', views.lista_articulos_json, name='lista-articulos-json'),
    url(r'^ver_articulo_json/$', views.ver_articulo_json, name='ver-articulo-json'),
    url(r'^lista_promociones/$', views.lista_promociones_view, name='lista-promociones'),
    url(r'^lista_promociones_json/$', views.lista_promociones_json, name='lista-promociones-json'),
    url(r'^lista_promocion_json/$', views.ver_promocion_json, name='ver-promocion-json'),

    # url(r'^productos_con_codigo_zooper_json/$', views.productos_con_codigo_zooper_json, name='productos-con-codigo-zooper-json')
]