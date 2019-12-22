# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from producto.models import ProductoZooper, ProductoTelemercado
from common import utils_bdd as bdd

class ManagerProductoTelemercado(object):
    """
        Clase para administrar los producto
    """
    clase = 'ProductoTelemercado'
    titulo = 'Supermercado Telemercado'
    supermercado = 'telemercado'

#    def __init__(self, titulo):
        #self.titulo = titulo
    @staticmethod
    def obtenerProducto(id):
        """
            Función que obtiene el ProductoTelemercado
            Param:
                id: id del producto
            Return:
                ProductoTelemercado
                None en caso de no existir el ProductoTelemercado
        """
        try:
            return ProductoTelemercado.objects.get(id=id)
        except Exception,e:
            return None


    def obtenerProductos(self, **kwargs):
        """
            Función para recuperar productos telemercado
            Params:
                
            Return:
        """
        productos = ProductoTelemercado.objects.all()
        if 'ids' in kwargs:
            productos = productos.filter(id__in=kwargs['ids'])
        if 'codigo' in kwargs:
            productos = productos.filter(codigo=kwargs['codigo'])
        if 'codigos' in kwargs:
            productos = productos.filter(codigo__in=kwargs['codigos'])
        if 'titulo' in kwargs:
            productos = productos.filter(titulo=kwargs['titulo'])
        if 'titulos' in kwargs:
            productos = productos.filter(titulo__in=kwargs['titulos'])
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
        siguientes_producto = ProductoTelemercado.objects.filter(productozooper__isnull=True)[:cantidad]
        if (siguientes_producto.count() == 0):
            return None
        return siguientes_producto



    def coincidenciasZooper(self, productozooper_id):
        """
            Función que busca un ProductoZooper en el la tabla del supermercado correspondiente
        """
        productozooper = ProductoZooper.objects.get(id=productozooper_id)
        q_soundex = """SELECT * FROM producto_productotelemercado p WHERE soundex(p.titulo) = soundex('{}') OR p.titulo ILIKE '%{}%';""".format(productozooper.marca, productozooper.marca)
        resultados_soundex = bdd.ejecutar_consulta(q_soundex)

        lista_palabras_producto = unicode(productozooper.nombre_producto).split(' ')
        tope_max = len(lista_palabras_producto)
        productos_a_retornar = []
        for producto_otro_supermercado in resultados_soundex:
            #print producto_otro_supermercado
            puntajes_prod = list()
            puntaje = 0
            for palabra in lista_palabras_producto:
                productos_puntaje = ProductoTelemercado.objects.filter(
                    codigo = producto_otro_supermercado['codigo'],
                    titulo__icontains = palabra,
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
        return 'https://www.telemercados.cl/busca/?ft='+unicode(producto.codigo)
        #return 'https://www.telemercados.cl/Sistema/buscavazia?ft='+unicode(producto.codigo)


    def desvincularProducto(self, productozooper_id):
        """
            Funcion que borra todos los productos azociados a id de zooper
        """
        productos = self.obtenerProductos(productozooper_id=productozooper_id)
        for producto in productos:
            producto.productozooper_id = None
            producto.save()