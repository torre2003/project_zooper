# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

from supermercado import configuraciones

class ArticuloLider(models.Model):
    codigo = models.CharField(max_length=40, null=True)

    nombre = models.CharField(max_length=300, null=True)
    marca = models.CharField(max_length=100, null=True)
    url_imagen = models.CharField(max_length=300, null=True)
    url_producto = models.CharField(max_length=300, null=True)

    caracteristica = models.CharField(max_length=50, null=True)
    precio_alto = models.IntegerField(default=0)
    precio_bajo = models.IntegerField(default=0)
    precio_unidad_medida = models.CharField(max_length=50, null=True)

    etiquetas_precio = JSONField(null=True, default={})
    etiquetas_oferta = JSONField(null=True, default={})
    
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_PRODUCTO, null=True)
    estado_mensaje = models.CharField(max_length=100, null=True)



class InfoActualizacionArticuloLider(models.Model):
    articulolider = models.OneToOneField(ArticuloLider, models.DO_NOTHING, null=True)
    url_actualizacion = models.CharField(max_length=300, null=True)
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_ACTUALIZACION, null=True)
    estado_mensaje = models.CharField(max_length=100, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)


class InfoBusquedaArticuloLider(models.Model):
    url_busqueda = models.CharField(max_length=300, null=True)
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_BUSQUEDA, null=True)
    intentos = models.IntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)
