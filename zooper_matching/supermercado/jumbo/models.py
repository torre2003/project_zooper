# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

from supermercado import configuraciones

class ArticuloJumbo(models.Model):
    # identificadores jumbo
    producto_id = models.CharField(max_length=20, null=True)            #productId
    codigo_referencia = models.CharField(max_length=20, null=True)      #productReference
    item_id = models.CharField(max_length=20, null=True)                #items:0:itemId
    ean = models.CharField(max_length=20, null=True)                    #items:0:ean

    nombre = models.CharField(max_length=300, null=True)                #productName
    marca = models.CharField(max_length=100, null=True)                 #brand
    url_imagen = models.CharField(max_length=200, null=True)            #items:images:0:imageUrl
    url_producto = models.CharField(max_length=200, null=True)          #link

    data_producto = JSONField(null=True, default={})                                         #ProductData:0
    data_sku = JSONField(null=True, default={})                                              #SkuData:0

    precio = models.IntegerField(default=0)                             #items:0:sellers:0:commertialOffer:Price
    precio_sin_descuento = models.IntegerField(default=0)               #items:0:sellers:0:commertialOffer:PriceWithoutDiscount
    validez_precio = models.DateTimeField(null=True)            #items:0:sellers:0:commertialOffer:PriceValidUntil
    cantidad_disponible = models.IntegerField(default=0)                #items:0:sellers:0:commertialOffer:AvailableQuantity
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_PRODUCTO, null=True)
    estado_mensaje = models.CharField(max_length=100, null=True)


class PromocionJumbo(models.Model):
    habilitada = models.BooleanField(default=False)
    promocion_id = models.CharField(max_length=20, null=True)           #key del diccionario
    nombre = models.CharField(max_length=200, null=True)                #name
    grupo = models.CharField(max_length=200, null=True)                 #grupo
    tipo = models.CharField(max_length=200, null=True)                  #type
    tipo_descuento = models.CharField(max_length=200, null=True)        #discountType
    tipo_promocion = models.CharField(max_length=200, null=True)        #promotionType
    valor = models.CharField(max_length=200, null=True)                 #value
    fecha_inicio = models.DateTimeField(auto_now_add=True)              #start
    fecha_final = models.DateTimeField(auto_now_add=True)               #end
    dias_disponible = JSONField(null=True, default={})                                       #availableDays
    cantidad = models.IntegerField(default=0, null=True)                           #quantity
    cantidad_afectada = models.IntegerField(default=0, null=True)                  #quantityAffected
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_PRODUCTO, null=True)
    estado_mensaje = models.CharField(max_length=100, null=True)


class InfoActualizacionArticuloJumbo(models.Model):
    _url_actualizacion = 'https://nuevo.jumbo.cl/api/catalog_system/pub/products/search/?fq=productId%3A'#  7203  <---- remplazar por id de producto
    articulojumbo = models.OneToOneField(ArticuloJumbo, models.DO_NOTHING, null=True)
    identificador_busqueda = models.CharField(max_length=20, null=True)                  #como identificado se usara "producto_id"
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_ACTUALIZACION, null=True)
    estado_mensaje = models.CharField(max_length=100, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)

    def get_url_actualizacion(self):
        return self._url_actualizacion + unicode (self.identificador_busqueda)

    def set_url_actualizacion(self, value):
        pass
    url_actualizacion = property(get_url_actualizacion, set_url_actualizacion)

class InfoBusquedaArticuloJumbo(models.Model):
    identificador_busqueda = models.CharField(max_length=20, null=True)                  #como identificado se usara "producto_id"
    estado = models.CharField(max_length=30,choices=configuraciones.ESTADOS_BUSQUEDA, null=True)
    intentos = models.IntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now_add=True)
