# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from producto.models import ProductoZooper, ProductoTottus
from common import utils_bdd as bdd

class ManagerProductoTottus(object):
    """
        Clase para administrar los producto
    """
    clase = 'ProductoTottus'
    titulo = 'Supermercado Tottus'
    supermercado = 'tottus'

#    def __init__(self, titulo):
        #self.titulo = titulo

    @staticmethod
    def obtenerProducto(id):
        """
            Función que obtiene el ProductoTottus
            Param:
                id: id del producto
            Return:
                ProductoTottus
                None en caso de no existir el ProductoTottus
        """
        try:
            return ProductoTottus.objects.get(id=id)
        except Exception,e:
            return None

    def obtenerProductos(self, **kwargs):
        """
            Función para recuperar productos telemercado
            Params:
                
            Return:
        """
        productos = ProductoTottus.objects.all()
        if 'ids' in kwargs:
            productos = productos.filter(id__in=kwargs['ids'])
        if 'codigo' in kwargs:
            productos = productos.filter(codigo=kwargs['codigo'])
        if 'codigos' in kwargs:
            productos = productos.filter(codigo__in=kwargs['codigos'])
        if 'nombre' in kwargs:
            productos = productos.filter(nombre=kwargs['nombre'])
        if 'nombres' in kwargs:
            productos = productos.filter(nombre__in=kwargs['nombres'])
        if 'marca' in kwargs:
            productos = productos.filter(marca=kwargs['marca'])
        if 'marcas' in kwargs:
            productos = productos.filter(marca__in=kwargs['marcas'])
        if 'productozooper_id' in kwargs:
            productos = productos.filter(productozooper_id=kwargs['productozooper_id'])
        if 'productozooper_ids' in kwargs:
            productos = productos.filter(productozooper_id__in=kwargs['productozooper_ids'])
        if 'limit' in kwargs:
            productos = productos[:kwargs['limit']]
        return productos

    def siguienteProducto(self, cantidad=1):
        """
            retorna el siguiente producto sin codigo zooper asociado
            return:
                Array<ProductoJumbo>, null si no quedan productos
        """
        siguientes_producto = ProductoTottus.objects.filter(productozooper__isnull=True)[:cantidad]
        if (siguientes_producto.count() == 0):
            return None
        return siguientes_producto



    def coincidenciasZooper(self, productozooper_id):
        """
            Función que busca un ProductoZooper en el la tabla del supermercado correspondiente
        """
        productozooper = ProductoZooper.objects.get(id=productozooper_id)
        q_soundex = """SELECT * FROM producto_productotottus p WHERE soundex(p.marca) = soundex('{}');""".format(productozooper.marca)
        resultados_soundex = bdd.ejecutar_consulta(q_soundex)

        lista_palabras_producto = unicode(productozooper.nombre_producto).split(' ')
        tope_max = len(lista_palabras_producto)
        productos_a_retornar = []
        for producto_otro_supermercado in resultados_soundex:
            #print producto_otro_supermercado
            puntajes_prod = list()
            puntaje = 0
            for palabra in lista_palabras_producto:
                productos_puntaje = ProductoTottus.objects.filter(
                    codigo = producto_otro_supermercado['codigo'],
                    nombre__icontains = palabra,
                )
                if productos_puntaje.count() > 0:
                    puntaje += 1
            if puntaje != 0:
                producto_otro_supermercado['puntaje'] = puntaje
                productos_a_retornar.append(producto_otro_supermercado)
        return productos_a_retornar


    def vincularProducto (self,producto_id, productozooper_id):
        producto = self.obtenerProducto(producto_id)
        if producto is None:
            raise Exception ('No existe el tipo de alojamiento')
        producto.productozooper_id = productozooper_id
        producto.save()

    @staticmethod
    def obtenerLinkProducto (producto):
        return 'http://www.tottus.cl'+producto.link


    def desvincularProducto(self, productozooper_id):
        """
            Funcion que borra todos los productos azociados a id de zooper
        """
        productos = self.obtenerProductos(productozooper_id=productozooper_id)
        for producto in productos:
            producto.productozooper_id = None
            producto.save()