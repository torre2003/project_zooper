# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from producto.models import ProductoZooper

class ManagerProductoZooper():
    """
        Clase para administrar los producto
    """
    clase = 'ProductoZooper'
    titulo = 'Zooper'
    supermercado = 'Zooper'

    @staticmethod
    def obtenerProducto(id):
        """
            Función que obtiene el ProductoZooper
            Param:
                id: id del producto
            Return:
                ProductoZooper
                None en caso de no existir el ProductoZooper
        """
        try:
            return ProductoZooper.objects.get(id=id)
        except Exception,e:
            return None

    def obtenerProductos(self, **kwargs):
        """
            Función para recuperar productos zoooper
            Params:
                
            Return:
        """
        productos = ProductoZooper.objects.all()
        if 'ids' in kwargs:
            productos = productos.filter(id__in=kwargs['ids'])
        if 'url' in kwargs:
            productos = productos.filter(url=kwargs['url'])
        if 'marca' in kwargs:
            productos = productos.filter(marca=kwargs['marca'])
        if 'marcas' in kwargs:
            productos = productos.filter(marca__in=kwargs['marcas'])
        if 'nombre_producto' in kwargs:
            productos = productos.filter(nombre_producto=kwargs['nombre_producto'])
        if 'nombre_productos' in kwargs:
            productos = productos.filter(nombre_producto__in=kwargs['nombre_productos'])
        if 'limit' in kwargs:
            productos = productos[:kwargs['limit']]
        return productos

    