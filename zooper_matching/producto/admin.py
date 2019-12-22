# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import ProductoLider, ProductoJumbo, ProductoTelemercado, ProductoTottus, ProductoZooper


class ProductosZooper(admin.ModelAdmin):
    list_display = ['nombre_producto', 'marca', ]

admin.site.register(ProductoZooper,ProductosZooper)


class ProductosLider(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', ]

admin.site.register(ProductoLider,ProductosLider)



class ProductosJumbo(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', ]

admin.site.register(ProductoJumbo,ProductosJumbo)



class ProductosTelemercado(admin.ModelAdmin):
    list_display = ['codigo', 'titulo', ]

admin.site.register(ProductoTelemercado,ProductosTelemercado)



class ProductosTottus(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', ]

admin.site.register(ProductoTottus,ProductosTottus)