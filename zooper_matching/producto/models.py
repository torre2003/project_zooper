# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

NO_ACTUALIZADA = 'NO_ACTUALIZADO'
ACTUALIZADA = 'ACTUALIZADA'
PENDIENTE_ACTUALIZACION = 'PENDIENTE_ACTUALIZACION'
ERROR = 'ERROR'
ERROR_PRECIO = 'ERROR_PRECIO'
SIN_PRECIO = 'SIN_PRECIO'
ESTADOS_PRODUCTOS = (
    (NO_ACTUALIZADA, 'NO_ACTUALIZADO'),
    (ACTUALIZADA, 'ACTUALIZADA'),
    (PENDIENTE_ACTUALIZACION, 'PENDIENTE_ACTUALIZACION'),
    (ERROR, 'ERROR'),
    (ERROR_PRECIO, 'ERROR_PRECIO'),
    (SIN_PRECIO, 'SIN_PRECIO'),
)

class ProductoZooper(models.Model):
    medida = models.CharField(max_length=50, null=True)#Caracteristica en lider
    precio = models.CharField(max_length=15, null=True)#
    precio_unidad_medida = models.CharField(max_length=25, null=True)#
    nombre_producto = models.CharField(max_length=100, null=True)#Sub_titulo en Lider
    marca = models.CharField(max_length=50, null=True)#Titulo en Lider
    url = models.CharField(max_length=300, null=True)#


class ProductoLider(models.Model):
    codigo = models.CharField(max_length=20, null=True)
    caracteristica = models.CharField(max_length=50, null=True)
    precio = models.CharField(max_length=15, null=True)
    precio_unidad_medida = models.CharField(max_length=25, null=True)
    sub_titulo = models.CharField(max_length=100, null=True)
    titulo = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=200, null=True)
    productozooper = models.ForeignKey(ProductoZooper, models.DO_NOTHING, null=True)
    """
        Gestión de actualización de precios
    """
    ultima_actualizacion = models.DateTimeField(default=datetime.now())
    estado = models.CharField(max_length=30,choices=ESTADOS_PRODUCTOS, null=True)



class ProductoJumbo(models.Model):
    codigo = models.CharField(max_length=20, null=True)
    image_urls = models.CharField(max_length=200, null=True)
    marca = models.CharField(max_length=50, null=True)
    precio = models.CharField(max_length=20, null=True)
    titulo = models.CharField(max_length=1000, null=True)
    url = models.CharField(max_length=200, null=True)
    productozooper = models.ForeignKey(ProductoZooper, models.DO_NOTHING, null=True)
    """
        Gestión de actualización de precios
    """
    ultima_actualizacion = models.DateTimeField(default=datetime.now())
    estado = models.CharField(max_length=30,choices=ESTADOS_PRODUCTOS, null=True)


class ProductoTelemercado(models.Model):
    codigo = models.CharField(max_length=20, null=True)
    detalle = models.CharField(max_length=1000, null=True)
    precio = models.CharField(max_length=20, null=True)
    titulo = models.CharField(max_length=100, null=True)
    url_imagen = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=400, null=True)
    productozooper = models.ForeignKey(ProductoZooper, models.DO_NOTHING, null=True)
    """
        Gestión de actualización de precios
    """
    ultima_actualizacion = models.DateTimeField(default=datetime.now())
    estado = models.CharField(max_length=30,choices=ESTADOS_PRODUCTOS, null=True)


class ProductoTottus(models.Model):
    codigo = models.CharField(max_length=20, null=True)
    link = models.CharField(max_length=200, null=True)
    marca = models.CharField(max_length=40, null=True)
    medida = models.CharField(max_length=50, null=True)
    nombre = models.CharField(max_length=100, null=True)
    precio = models.CharField(max_length=10, null=True)
    productozooper = models.ForeignKey(ProductoZooper, models.DO_NOTHING, null=True)
    """
        Gestión de actualización de precios
    """
    ultima_actualizacion = models.DateTimeField(default=datetime.now())
    estado = models.CharField(max_length=30,choices=ESTADOS_PRODUCTOS, null=True)