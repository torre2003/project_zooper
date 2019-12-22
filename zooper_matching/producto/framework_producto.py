# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from producto.framework_zooper import ManagerProductoZooper
from producto.framework_jumbo import ManagerProductoJumbo
from producto.framework_telemercado import ManagerProductoTelemercado
from producto.framework_tottus import ManagerProductoTottus
from producto.framework_lider import ManagerProductoLider


class ManagerProducto():
    """
        Clase para gestionar la lectura de los productos en general
    """


    def obtenerProductosAsociadosAZooper(self, cantidad_minima_supermercados = 2, con_detalle=False):
        """
            Función que obtiene los productos zooper con una cantidad mayor o igual de productos
            de supermercados asociados a la pasada en los parametros
            Param:
                cantidad_minima_supermercados
            Return:
                {'productozooper_id':{
                    'manager.clase':{
                            id:productosupermercado_id,
                                SI CON DETALLE
                            'producto': <PRODUCTO>,
                            'supermercado': manager.supermercado,
                        }
                    }
                }c
        """
        manager_zooper = ManagerProductoZooper()
        manager_supermercados = []
        manager_supermercados.append(ManagerProductoJumbo())
        manager_supermercados.append(ManagerProductoTelemercado())
        manager_supermercados.append(ManagerProductoTottus())
        manager_supermercados.append(ManagerProductoLider())
        productos_zooper = {}
        for manager in manager_supermercados:
            productos = manager.obtenerProductos()
            productos.filter(productozooper__isnull=False)
            for producto in productos:
                if not producto.productozooper_id in productos_zooper:
                    productos_zooper[producto.productozooper_id] = {}
                productos_zooper[producto.productozooper_id][manager.clase] = {'id':producto.id}
                if con_detalle:
                    productos_zooper[producto.productozooper_id][manager.clase]['producto'] = producto
                    productos_zooper[producto.productozooper_id][manager.clase]['supermercado'] = manager.supermercado
        retorno = {}
        for productozooper_id in productos_zooper:
            if productozooper_id is not None and len(productos_zooper[productozooper_id]) >= cantidad_minima_supermercados:
                retorno[productozooper_id] = productos_zooper[productozooper_id]
        return retorno


    def generarArregloJSONEcommerce(self, cantidad_minima_supermercados = 2):
        """
            Función que genera el arreglo json con el formato requerido para el ecommerce en wordpress
            Param:

            Return:
            [
                {
                    "cod_zooper": "1",
                    "titulo": "Leche 1L",
                    "imagen": "https://jumbo.vteximg.com.br/arquivos/ids/164822-1500-1500/302773.jpg",
                    "precios": {
                        "zooper": "1290",
                        "lider": "1590",
                        "unimarc": "1390",
                        "jumbo": "1390",
                        "santa_isabel": "1290"
                    }
                },
            ]
        """
        retorno = []
        productos = self.obtenerProductosAsociadosAZooper(cantidad_minima_supermercados = 2, con_detalle=True)
        for productozooper_id in productos:
            productozooper = ManagerProductoZooper.obtenerProducto(productozooper_id)
            aux = {}
            aux['cod_zooper'] = unicode(productozooper_id)
            aux['titulo'] = productozooper.nombre_producto+'  |  '+productozooper.marca
            aux['imagen'] = 'https://jumbo.vteximg.com.br/arquivos/ids/164822-1500-1500/302773.jpg'
            aux['precios'] = {
                'zooper':productozooper.precio
            }

            for supermercado in productos[productozooper_id]:
                precio = ''
                aux_precio = productos[productozooper_id][supermercado]['producto'].precio
                if supermercado == 'ProductoTelemercado':
                    aux_precio = aux_precio.replace('.','')
                    aux_precio = aux_precio.replace(' ','')
                    aux_precio = aux_precio.replace('Kg','')
                    precio = aux_precio
                elif supermercado == 'ProductoJumbo':
                    aux_precio = aux_precio.replace('$','')
                    aux_precio = aux_precio.replace('.','')
                    aux_precio = aux_precio.replace(',','.')
                    precio = unicode(int(float(aux_precio)))
                elif supermercado == 'ProductoLider':
                    precio = aux_precio
                elif supermercado == 'ProductoTottus':
                    aux_precio = aux_precio.replace('$','')
                    precio = aux_precio
                else:
                    precio = aux_precio
                print supermercado
                print precio
                aux['precios'][productos[productozooper_id][supermercado]['supermercado']] = precio
            retorno.append(aux)
        return retorno


    def obtenerProductosAActualizar(self):
        #manager = ManagerProducto()
        productos = self.obtenerProductosAsociadosAZooper(cantidad_minima_supermercados=2, con_detalle=False)
        manager_supermercados = {
            'ProductoJumbo':ManagerProductoJumbo(),
            'ProductoTelemercado':ManagerProductoTelemercado(),
            'ProductoTottus':ManagerProductoTottus(),
            'ProductoLider':ManagerProductoLider(),
        }
        productos_retorno = []
        for productozooper_id in productos:
            for supermercado in productos[productozooper_id]:
                productosupermercado = manager_supermercados[supermercado].obtenerProducto(productos[productozooper_id][supermercado]['id'])
                productos_retorno.append({
                    'productozooper_id':productozooper_id,
                    'supermercado':manager_supermercados[supermercado].supermercado,
                    'productosupermercado_id':productos[productozooper_id][supermercado]['id'],
                    'url':manager_supermercados[supermercado].obtenerLinkProducto(productosupermercado)
                            })
        return productos_retorno









