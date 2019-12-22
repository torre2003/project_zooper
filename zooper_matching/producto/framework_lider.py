# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from producto.models import ProductoZooper, ProductoLider
from common import utils_bdd as bdd

class ManagerProductoLider(object):
    """
        Clase para administrar los producto
    """
    clase = 'ProductoLider'
    titulo = 'Supermercado Lider'
    supermercado = 'lider'

#    def __init__(self, titulo):
        #self.titulo = titulo

    @staticmethod
    def obtenerProducto(id):
        """
            Función que obtiene el ProductoLider
            Param:
                id: id del producto
            Return:
                ProductoLider
                None en caso de no existir el ProductoLider
        """
        try:
            return ProductoLider.objects.get(id=id)
        except Exception,e:
            return None

    def obtenerProductos(self, **kwargs):
        """
            Función para recuperar productos telemercado
            Params:
                
            Return:
        """
        productos = ProductoLider.objects.all()
        if 'ids' in kwargs:
            productos = productos.filter(id__in=kwargs['ids'])
        if 'codigo' in kwargs:
            productos = productos.filter(codigo=kwargs['codigo'])
        if 'codigos' in kwargs:
            productos = productos.filter(codigo__in=kwargs['codigos'])
        if 'titulo' in kwargs:
            productos = productos.filter(nombre=kwargs['titulo'])
        if 'titulos' in kwargs:
            productos = productos.filter(nombre__in=kwargs['titulos'])
        if 'sub_titulo' in kwargs:
            productos = productos.filter(nombre=kwargs['sub_titulo'])
        if 'sub_titulos' in kwargs:
            productos = productos.filter(nombre__in=kwargs['sub_titulos'])
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
        siguientes_producto = ProductoLider.objects.filter(productozooper__isnull=True)[:cantidad]
        if (siguientes_producto.count() == 0):
            return None
        return siguientes_producto



    def coincidenciasZooper(self, productozooper_id):
        """
            Función que busca un ProductoZooper en el la tabla del supermercado correspondiente
        """
        productozooper = ProductoZooper.objects.get(id=productozooper_id)
        q_soundex = """SELECT * FROM producto_productolider p WHERE soundex(p.titulo) = soundex('{}');""".format(productozooper.marca)
        resultados_soundex = bdd.ejecutar_consulta(q_soundex)

        lista_palabras_producto = unicode(productozooper.nombre_producto).split(' ')
        tope_max = len(lista_palabras_producto)
        productos_a_retornar = []
        for producto_otro_supermercado in resultados_soundex:
            #print producto_otro_supermercado
            puntajes_prod = list()
            puntaje = 0
            for palabra in lista_palabras_producto:
                productos_puntaje = ProductoLider.objects.filter(
                    codigo = producto_otro_supermercado['codigo'],
                    sub_titulo__icontains = palabra,
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
            raise Exception ('No existe el producto')
        producto.productozooper_id = productozooper_id
        producto.save()


    def desvincularProducto(self, productozooper_id):
        """
            Funcion que borra todos los productos azociados a id de zooper
        """
        productos = self.obtenerProductos(productozooper_id=productozooper_id)
        for producto in productos:
            producto.productozooper_id = None
            producto.save()


    @staticmethod
    def obtenerLinkProducto (producto):
        return producto.url