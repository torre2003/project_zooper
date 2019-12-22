# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from apps import MatchingConfig


app_name = MatchingConfig.name

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^matching_productos_supermercado_especifico/$', views.matching_productos_supermercado_especifico_view, name='matching-productos-supermercado-especifico-view'),
    url(r'^matching_productos_supermercado_especifico_json/$', views.consulta_producto_supermercado_especifico_json, name='consulta-producto-supermercado-especifico-json'),
    url(r'^matching_productos_supermercado_zooper/$', views.matching_productos_supermercado_zooper_view, name='matching-productos-supermercado-zooper-view'),
    url(r'^matching_producto_supermercado_zooper_json/$', views.consulta_producto_supermercado_zooper_json, name='consulta-producto-supermercado-zooper-json'),
    url(r'^vincular_producto_supermercado_zooper_json/$', views.vincular_producto_supermercado_zooper_json, name='vincular-producto-supermercado-zooper-json'),
    #url(r'^sin-permisos/$', views.sin_permisos, name='sin-permisos'),

]