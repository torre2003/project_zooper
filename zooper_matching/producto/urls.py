# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from . import views_gestion_actualizacion
from apps import ProductoConfig


app_name = ProductoConfig.name

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^productos_con_codigo_zooper/$', views.productos_con_codigo_zooper_view, name='productos-con-codigo-zooper'),
    url(r'^productos_con_codigo_zooper_json/$', views.productos_con_codigo_zooper_json, name='productos-con-codigo-zooper-json'),
    url(r'^obtener_productos_a_actualizar_json/$', views_gestion_actualizacion.obtener_productos_a_actualizar_json, name='productos-con-codigo-zooper-json'),
    url(r'^actualizacion_registro_producto_json/$', views_gestion_actualizacion.actualizacion_registro_producto_json, name='actualizacion-registro-producto-json'),

    url(r'^obtener_productos_custom_json/$', views_gestion_actualizacion.obtener_productos_custom_json, name='obtener-productos-custom-json'),
    url(r'^actualizacion_producto_custom_json/$', views_gestion_actualizacion.actualizacion_producto_custom_json, name='actualizacion-producto-custom-json'),
    #url(r'^sin-permisos/$', views.sin_permisos, name='sin-permisos'),
]