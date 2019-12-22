# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import pytz
utc=pytz.UTC

from datetime import datetime
from django.db import transaction

from models import ArticuloJumbo, PromocionJumbo, InfoActualizacionArticuloJumbo, InfoBusquedaArticuloJumbo
from supermercado.framework_supermercado import ManagerLogSupermercado



class ManagerArticuloJumbo(object):
    """
        Clase para administrar los producto
    """
    clase = 'ArticuloJumbo'
    titulo = 'Supermercado Jumbo'
    supermercado = 'jumbo'
    clases = {
        'ARTICULO':'ArticuloJumbo',
        'PROMOCION':'PromocionJumbo',
        'INFO_ACTUALIZACION':'InfoActualizacionArticuloJumbo',
        'INFO_BUSQUEDA':'InfoBusquedaArticuloJumbo',
    }

    #####################################################
    #######  ArticuloJumbo
    ####################################################

    @staticmethod
    def obtenerArticulo(id):
        """
            Función que obtiene el ArticuloJumbo según su id
            Param:
                id: id del producto
            Return:
                ArticuloJumbo
                None en caso de no existir el ProductoJumbo
        """
        try:
            return ArticuloJumbo.objects.get(id=id)
        except Exception,e:
            return None

    @staticmethod
    def obtenerArticulos(**kwargs):
        """
            Función para recuperar ArticulosJumbo
            Params:
                
            Return:
        """
        articulo = ArticuloJumbo.objects.all()
        if 'id' in kwargs:
            articulo = articulo.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            articulo = articulo.filter(id__in=kwargs['ids'])

        if 'producto_id' in kwargs:
            articulo = articulo.filter(producto_id=kwargs['producto_id'])
        if 'productos_id' in kwargs:
            articulo = articulo.filter(producto_id__in=kwargs['productos_id'])
        
        if 'codigo_referencia' in kwargs:
            articulo = articulo.filter(codigo_referencia=kwargs['codigo_referencia'])
        if 'codigos_referencia' in kwargs:
            articulo = articulo.filter(codigo_referencia__in=kwargs['codigos_referencia'])
        
        if 'item_id' in kwargs:
            articulo = articulo.filter(item_id=kwargs['item_id'])
        if 'items_id' in kwargs:
            articulo = articulo.filter(item_id__in=kwargs['items_id'])

        if 'ean' in kwargs:
            articulo = articulo.filter(ean=kwargs['ean'])
        if 'eans' in kwargs:
            articulo = articulo.filter(ean__in=kwargs['eans'])

        if 'nombre' in kwargs:
            articulo = articulo.filter(nombre=kwargs['nombre'])
        if 'nombres' in kwargs:
            articulo = articulo.filter(nombre__in=kwargs['nombres'])

        if 'marca' in kwargs:
            articulo = articulo.filter(marca=kwargs['marca'])
        if 'marcas' in kwargs:
            articulo = articulo.filter(marca__in=kwargs['marcas'])

        if 'url_producto' in kwargs:
            articulo = articulo.filter(url_producto=kwargs['url_producto'])
        if 'urls_producto' in kwargs:
            articulo = articulo.filter(urls_producto__in=kwargs['urls_producto'])

        if 'estado' in kwargs:
            articulo = articulo.filter(estado=kwargs['estado'])
        if 'estados' in kwargs:
            articulo = articulo.filter(estados__in=kwargs['estados'])
        if 'order_by' in kwargs:
            articulo = articulo.order_by(kwargs['order_by'])
        if 'limit' in kwargs:
            articulo = articulo[:kwargs['limit']]
        return articulo


    @staticmethod 
    def crearArticuloJumbo(producto_id, codigo_referencia, item_id, ean, nombre, marca, url_imagen, url_producto, data_producto, 
                            data_sku, precio, precio_sin_descuento, validez_precio, cantidad_disponible, estado, estado_mensaje, user_id=None):
        """
            Función que ingresa un nuevo ArticuloJumbo
            Param:
                <Char>producto_id             #productId
                <Char>codigo_referencia       #productReference
                <Char>item_id                 #items:0:itemId
                <Char>ean                     #items:0:ean

                <Char>nombre                  #productName
                <Char>marca                   #brand
                <Char>url_imagen              #items:images:0:imageUrl
                <Char>url_producto            #link

                <Json>data_producto           #ProductData:0
                <Json>data_sku                #SkuData:0

                <Integer>precio                 #items:0:sellers:0:commertialOffer:Price
                <Integer>precio_sin_descuento   #items:0:sellers:0:commertialOffer:PriceWithoutDiscount
                <Datetime>validez_precio        #items:0:sellers:0:commertialOffer:PriceValidUntil
                <Integer>cantidad_disponible    #items:0:sellers:0:commertialOffer:AvailableQuantity
                <Char>estado 
                <Char>estado_mensaje 
            Return:
                ArticuloJumbo
                None en caso de existir el articulo Jumbo en la base de datos
        """

        if len(ManagerArticuloJumbo.obtenerArticulos(producto_id=producto_id)) > 0:
            return None
        if len(ManagerArticuloJumbo.obtenerArticulos(codigo_referencia=codigo_referencia)) > 0:
            return None
        if len(ManagerArticuloJumbo.obtenerArticulos(item_id=item_id)) > 0:
            return None
        if len(ManagerArticuloJumbo.obtenerArticulos(ean=ean)) > 0:
            return None
        if len(ManagerArticuloJumbo.obtenerArticulos(nombre=nombre,marca=marca)) > 0:
            return None

        aux_articulojumbo = ArticuloJumbo(
            producto_id=producto_id,
            codigo_referencia=codigo_referencia,
            item_id=item_id,
            ean=ean,
            nombre=nombre,
            marca=marca,
            url_imagen=url_imagen,
            url_producto=url_producto,
            data_producto=data_producto,
            data_sku=data_sku,
            precio=precio,
            precio_sin_descuento=precio_sin_descuento,
            validez_precio=validez_precio,
            cantidad_disponible=cantidad_disponible,
            estado=estado,
            estado_mensaje=estado_mensaje
        )

        aux_articulojumbo.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloJumbo.supermercado,
            tipo=ManagerArticuloJumbo.clases['ARTICULO'],
            status='INFO',
            info= {'mensaje':'Producto {} [producto_id] ingresado'.format(producto_id)},
            modelo_id=aux_articulojumbo.id,
            user_id=user_id
        )
        ManagerArticuloJumbo.actualizarInfoActualizacionArticuloJumbo(aux_articulojumbo.id, estado='ACTUALIZADO', estado_mensaje='Creación articulo', user_id=user_id)
        return aux_articulojumbo



    @staticmethod 
    def editarArticuloJumbo(articulojumbo, producto_id=None, codigo_referencia=None, item_id=None, ean=None, nombre=None, marca=None, url_imagen=None, url_producto=None,
                        data_producto=None, data_sku=None, precio=None, precio_sin_descuento=None, validez_precio=None, cantidad_disponible=None, estado=None,
                        estado_mensaje=None, user_id=None):
        """
            Función EDITAR un ArticuloJumbo
            Param:
                <Integer>(articulojumbo_id) o <Char>producto_id o <ArticuloJumbo>
                <Char>producto_id             #productId
                <Char>codigo_referencia       #productReference
                <Char>item_id                 #items:0:itemId
                <Char>ean                     #items:0:ean

                <Char>nombre                  #productName
                <Char>marca                   #brand
                <Char>url_imagen              #items:images:0:imageUrl
                <Char>url_producto            #link

                <Json>data_producto           #ProductData:0
                <Json>data_sku                #SkuData:0

                <Integer>precio                 #items:0:sellers:0:commertialOffer:Price
                <Integer>precio_sin_descuento   #items:0:sellers:0:commertialOffer:PriceWithoutDiscount
                <Datetime>validez_precio        #items:0:sellers:0:commertialOffer:PriceValidUntil
                <Integer>cantidad_disponible    #items:0:sellers:0:commertialOffer:AvailableQuantity
                <Char>estado 
                <Char>estado_mensaje 
                <Integer> user id
            Return:
                ArticuloJumbo
                None en caso de existir el articulo Jumbo en la base de datos
        """
        aux_articulojumbo = None
        if type(articulojumbo) == type(1):
            aux_articulojumbo = ManagerArticuloJumbo.obtenerArticulo(articulojumbo)
        elif type(articulojumbo) == type('string'):
            aux_articulojumbo = ManagerArticuloJumbo.obtenerArticulos(producto_id=articulojumbo)
            if aux_articulojumbo.count() > 0:
                aux_articulojumbo = aux_articulojumbo[0]
        elif type(articulojumbo) == type(ArticuloJumbo()):
            aux_articulojumbo = articulojumbo
        articulojumbo = aux_articulojumbo
        if articulojumbo is None:
            return None
        info = {}
        if producto_id is not None:
            if articulojumbo.producto_id != producto_id:
                info['producto_id'] = articulojumbo.producto_id+' -> '+producto_id
                articulojumbo.producto_id = producto_id
        if codigo_referencia is not None:
            if articulojumbo.codigo_referencia != codigo_referencia:
                info['codigo_referencia'] = articulojumbo.codigo_referencia+' -> '+codigo_referencia
                articulojumbo.codigo_referencia = codigo_referencia
        if item_id is not None:
            if articulojumbo.item_id != item_id:
                info['item_id'] = articulojumbo.item_id+' -> '+item_id
                articulojumbo.item_id = item_id
        if ean is not None:
            if articulojumbo.ean != ean:
                info['ean'] = articulojumbo.ean+' -> '+ean
                articulojumbo.ean = ean
        if nombre is not None:
            if articulojumbo.nombre != nombre:
                info['nombre'] = articulojumbo.nombre+' -> '+nombre
                articulojumbo.nombre = nombre
        if marca is not None:
            if articulojumbo.marca != marca:
                info['marca'] = articulojumbo.marca+' -> '+marca
                articulojumbo.marca = marca
        if url_imagen is not None:
            if articulojumbo.url_imagen != url_imagen:
                info['url_imagen'] = articulojumbo.url_imagen+' -> '+url_imagen
                articulojumbo.url_imagen = url_imagen
        if url_producto is not None:
            if articulojumbo.url_producto != url_producto:
                info['url_producto'] = articulojumbo.url_producto+' -> '+url_producto
                articulojumbo.url_producto = url_producto
        if data_producto is not None:
            if articulojumbo.data_producto != data_producto:
                info['data_producto'] = articulojumbo.data_producto+' -> '+data_producto
                articulojumbo.data_producto = data_producto
        if data_sku is not None:
            if articulojumbo.data_sku != data_sku:
                info['data_sku'] = articulojumbo.data_sku+' -> '+data_sku
                articulojumbo.data_sku = data_sku
        if precio is not None:
            if articulojumbo.precio != precio:
                info['precio'] = articulojumbo.precio+' -> '+precio
                articulojumbo.precio = precio
        if precio_sin_descuento is not None:
            if articulojumbo.precio_sin_descuento != precio_sin_descuento:
                info['precio_sin_descuento'] = articulojumbo.precio_sin_descuento+' -> '+precio_sin_descuento
                articulojumbo.precio_sin_descuento = precio_sin_descuento
        if validez_precio is not None:
            aux_1 = articulojumbo.validez_precio.replace(tzinfo=utc)
            aux_2 = validez_precio.replace(tzinfo=utc)
            if aux_1 != aux_2:
                info['validez_precio'] = unicode(articulojumbo.validez_precio)+' -> '+unicode(validez_precio)
                articulojumbo.validez_precio = validez_precio
        if cantidad_disponible is not None:
            if articulojumbo.cantidad_disponible != cantidad_disponible:
                info['cantidad_disponible'] = articulojumbo.cantidad_disponible+' -> '+cantidad_disponible
                articulojumbo.cantidad_disponible = cantidad_disponible
        if estado is not None:
            if articulojumbo.estado != estado:
                info['estado'] = articulojumbo.estado+' -> '+estado
                articulojumbo.estado = estado
        if estado_mensaje is not None:
            if articulojumbo.estado_mensaje != estado_mensaje:
                info['estado_mensaje'] = articulojumbo.estado_mensaje+' -> '+estado_mensaje
                articulojumbo.estado_mensaje = estado_mensaje
        articulojumbo.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloJumbo.supermercado,
            tipo=ManagerArticuloJumbo.clases['ARTICULO'],
            status='INFO',
            info=info,
            user_id=user_id,
            modelo_id=articulojumbo.id,
        )
        ManagerArticuloJumbo.actualizarInfoActualizacionArticuloJumbo(aux_articulojumbo.id, estado='ACTUALIZADO', estado_mensaje='', user_id=user_id)
        return articulojumbo



    @staticmethod
    def extraerDataArticuloJumboDesdeDiccionario(data):
        """
            Función para extraer los datos recogidos desde jumbo
            Param:
                <String>(JSON) <Diccionario> data: la estructura del diccionario desbe ser la misma
                         que la descripcion de productos proporcionada por Jumbo
            Return:
                <Diccionario> Este va con el nombre de los campos según el modelo ArticuloJumbo
                None en caso de existir el articulo Jumbo en la base de datos
        """
        if type(data) == type('string'):
            data = json.loads(data)
        producto_id = None 
        if 'productId' in data:
            if data['productId']:
                producto_id = data['productId']
        codigo_referencia = None 
        if 'productReference' in data:
            if data['productReference']:
                codigo_referencia = data['productReference']
        item_id = None 
        ean = None
        url_imagen = None
        precio_sin_descuento = None
        validez_precios = None
        cantidad_disponible = None
        precio = None
        if 'items' in data:
            if len(data['items']) > 0:
                if 'itemId' in data['items'][0]:
                    if data['items'][0]['itemId']:
                        item_id = data['items'][0]['itemId']
                if 'ean' in data['items'][0]:
                    if data['items'][0]['ean']:
                        ean = data['items'][0]['ean']
                try:
                    url_imagen = data['items'][0]['images'][0]['imageUrl']
                except Exception, e:
                    pass
                try:
                    precio_sin_descuento = int(data['items'][0]['sellers'][0]['commertialOffer']['PriceWithoutDiscount'])
                except Exception, e:
                    pass
                try:
                    validez_precios = datetime.strptime(data['items'][0]['sellers'][0]['commertialOffer']['PriceValidUntil'].replace("T", " "),"%Y-%m-%d %H,%M,%S")
                except Exception, e:
                    pass
                try:
                    cantidad_disponible = int(data['items'][0]['sellers'][0]['commertialOffer']['AvailableQuantity'])
                except Exception, e:
                    pass
                try:
                    precio = int(data['items'][0]['sellers'][0]['commertialOffer']['Price'])
                except Exception, e:
                    pass
        nombre = None 
        if 'productName' in data:
            if data['productName']:
                nombre = data['productName']
        marca = None 
        if 'brand' in data:
            if data['brand']:
                marca = data['brand']
        url_producto = None 
        if 'link' in data:
            if data['link']:
                url_producto = data['link']
        data_producto = None
        if 'ProductData' in data:
            if len(data['ProductData']) > 0:
                data_producto = json.loads(data['ProductData'][0])
        data_sku = None
        if 'ProductData' in data:
            if len(data['SkuData']) > 0:
                data_sku = json.loads(data['SkuData'][0])
        retorno = {
            'producto_id': producto_id,
            'codigo_referencia' : codigo_referencia,
            'item_id' : item_id,
            'ean' : ean,
            'nombre' : nombre,
            'marca': marca,
            'url_imagen' : url_imagen,
            'url_producto' : url_producto,
            'data_producto': data_producto,
            'data_sku': data_sku,
            'precio' : precio,
            'precio_sin_descuento': precio_sin_descuento,
            'validez_precio' : validez_precios,
            'cantidad_disponible' : cantidad_disponible,
        }
        return retorno


    @staticmethod
    def crearArticuloJumboDesdeDiccionario(data, user_id=None):
        """
            Función que ingresa un nuevo ArticuloJumbo desde un diccionario, la estructura 
            del diccionario desbe ser la misma que la descripcion de productos proporcionada por Jumbo
            Param:
                <string>  o <diccionario>(JSON con el formato de Jumbo)  data: 
            Return:
                ArticuloJumbo
                None en caso de existir el articulo Jumbo en la base de datos
        """
        dic_articulojumbo = None
        if type(data) == type({}) or type(data) == type(""):
            dic_articulojumbo = ManagerArticuloJumbo.extraerDataArticuloJumboDesdeDiccionario(data)
        else:
            raise Exception ("El parámetro data no es de tipo diccionario o string ")
        estado = 'OK'
        estado_mensaje = 'Ingresado nuevo articulo'

        nuevo_articulo = ManagerArticuloJumbo.crearArticuloJumbo(
            producto_id=dic_articulojumbo['producto_id'],
            codigo_referencia=dic_articulojumbo['codigo_referencia'],
            item_id=dic_articulojumbo['item_id'],
            ean=dic_articulojumbo['ean'],
            nombre=dic_articulojumbo['nombre'],
            marca=dic_articulojumbo['marca'],
            url_imagen=dic_articulojumbo['url_imagen'],
            url_producto=dic_articulojumbo['url_producto'],
            data_producto=dic_articulojumbo['data_producto'],
            data_sku=dic_articulojumbo['data_sku'],
            precio=dic_articulojumbo['precio'],
            precio_sin_descuento=dic_articulojumbo['precio_sin_descuento'],
            validez_precio=dic_articulojumbo['validez_precio'],
            cantidad_disponible=dic_articulojumbo['cantidad_disponible'],
            
            estado=estado,
            estado_mensaje=estado_mensaje,
            user_id=user_id,
        )
        if nuevo_articulo is None:
            ManagerLogSupermercado.crearLog(grupo=ManagerArticuloJumbo.supermercado, tipo=ManagerArticuloJumbo.clase, status='ERROR', info= {'mensaje':'El producto {} [producto_id] ya se encuentra ingresado'.format(producto_id)} , user_id=user_id)
        return nuevo_articulo


    @staticmethod
    def actualizarArticuloJumboDesdeDiccionario(data, user_id=None):
        """
            Función que actualiza un ArticuloJumbo existente en la base de datos desde un diccionario, la estructura 
            del diccionario desbe ser la misma que la descripcion de productos proporcionada por Jumbo
            Param:
                <string>(JSON con el formato de jubmo) o <diccionario> (Ya procesado) data: 
            Return:
                ArticuloJumbo
                None en caso de no existir el articulo Jumbo en la base de datos
        """
        dic_articulojumbo = None
        if type(data) == type({}) or type(data) == type(""):
            dic_articulojumbo = ManagerArticuloJumbo.extraerDataArticuloJumboDesdeDiccionario(data)
        else:
            raise Exception ("El parámetro data no es de tipo diccionario o string ")
        estado = 'OK'
        estado_mensaje = 'Articulo actualizado'


        articulojumbo = ManagerArticuloJumbo.editarArticuloJumbo(
            articulojumbo=dic_articulojumbo['producto_id'],
            producto_id=dic_articulojumbo['producto_id'],
            codigo_referencia=dic_articulojumbo['codigo_referencia'],
            item_id=dic_articulojumbo['item_id'],
            ean=dic_articulojumbo['ean'],
            nombre=dic_articulojumbo['nombre'],
            marca=dic_articulojumbo['marca'],
            url_imagen=dic_articulojumbo['url_imagen'],
            url_producto=dic_articulojumbo['url_producto'],
            data_producto=dic_articulojumbo['data_producto'],
            data_sku=dic_articulojumbo['data_sku'],
            precio=dic_articulojumbo['precio'],
            precio_sin_descuento=dic_articulojumbo['precio_sin_descuento'],
            validez_precio=dic_articulojumbo['validez_precio'],
            cantidad_disponible=dic_articulojumbo['cantidad_disponible'],
            estado=estado,
            estado_mensaje=estado_mensaje,
            user_id=user_id
        )
        if articulojumbo is None:
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloJumbo.supermercado,
                tipo=ManagerArticuloJumbo.clases['ARTICULO'],
                status='ERROR',
                info= {'mensaje':'El producto no existe {} [producto_id]'.format(producto_id)},
                user_id=user_id
            )
        return articulojumbo


    #####################################################
    #######  InfoActualizacionArticuloJumbo
    ####################################################


    @staticmethod
    def obtenerInfoActualizacionArticuloJumbo(id):
        """
            Función que obtiene el InfoActualizacionArticuloJumbo según su id
            Param:
                id: id del producto
            Return:
                InfoActualizacionArticuloJumbo
                None en caso de no existir el InfoActualizacionArticuloJumbo
        """
        try:
            return InfoActualizacionArticuloJumbo.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtenerInfosActualizacionArticuloJumbo(**kwargs):
        """
            Función para recuperar InfoActualizacionArticuloJumbo
            Params:
                id
                ids
                articulojumbo_id
                articulojumbo_ids
                estado
                estados
                limit
            Return:
        """
        infosactualizacionarticulojumbo = InfoActualizacionArticuloJumbo.objects.all()
        if 'id' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.filter(id__in=kwargs['ids'])

        if 'articulojumbo_id' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.filter(articulojumbo_id=kwargs['articulojumbo_id'])
        if 'articulojumbo_ids' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.filter(articulojumbo_id__in=kwargs['articulojumbo_ids'])

        if 'estado' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.filter(estado=kwargs['estado'])
        if 'estados' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.filter(estado__in=kwargs['estados'])
        if 'order_by' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo.order_by(kwargs['order_by'])
        if 'limit' in kwargs:
            infosactualizacionarticulojumbo = infosactualizacionarticulojumbo[:kwargs['limit']]
        return infosactualizacionarticulojumbo


    @staticmethod
    def actualizarInfoActualizacionArticuloJumbo(articulojumbo, estado, estado_mensaje, actualizar_fecha=True,
                                                identificador_busqueda=None, user_id=None):
        """
            Función que ingresa o actualiza la info de actualizacion de un ArticuloJumbo
            Param:
                <Integer> o <ArticuloJumbo> o <InfoActualizacionArticuloJumbo> articulojumbo
                <Char>estado   NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
                estado_mensaje
                identificador_busqueda identificador por el cual se realiza la actualizacion del articulo por defecto producto_id
                user_id
            Return:
                InfoActualizacionArticuloJumbo
                None en caso de existir el articulo Jumbo en la base de datos
        """
        info_actualizacion = None
        if type(articulojumbo) == type(1) or type(articulojumbo) == type(ArticuloJumbo()):
            if type(articulojumbo) == type(1):
                articulojumbo = ManagerArticuloJumbo.obtenerArticulo(articulojumbo)
            info_actualizacion =  ManagerArticuloJumbo.obtenerInfosActualizacionArticuloJumbo(articulojumbo_id=articulojumbo.id)
            if info_actualizacion.count() == 0:
                identificador_busqueda = articulojumbo.producto_id
                info_actualizacion = InfoActualizacionArticuloJumbo(
                    articulojumbo=articulojumbo,
                    identificador_busqueda=identificador_busqueda,
                    estado=estado,
                    estado_mensaje=estado_mensaje,
                )
                info_actualizacion.save()
                return info_actualizacion
            else:
                info_actualizacion = info_actualizacion[0]
        elif type(articulojumbo) == type(InfoActualizacionArticuloJumbo()):
            info_actualizacion = articulojumbo
        else:
            raise Exception('Tipo no corresponde')
        if articulojumbo is None:
            return None
        info_actualizacion.estado = estado
        info_actualizacion.estado_mensaje = estado_mensaje
        if actualizar_fecha:
            info_actualizacion.ultima_actualizacion = datetime.now()
        info_actualizacion.save()
        return info_actualizacion

    #####################################################
    #######  InfoBusquedaArticuloJumbo
    ####################################################

    @staticmethod
    def obtenerInfoBusquedaArticuloJumbo(id):
        """
            Función que obtiene el InfoBusquedaArticuloJumbo según su id
            Param:
                id: id de la busqueda
            Return:
                InfoBusquedaArticuloJumbo
                None en caso de no existir el InfoBusquedaArticuloJumbo
        """
        try:
            return InfoBusquedaArticuloJumbo.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtenerInfosBusquedaArticuloJumbo(**kwargs):
        """
            Función para recuperar InfoBusquedaArticuloJumbo
            Params:
                id
                ids
                estado
                estados
                identificador_busqueda
                identificadores_busqueda
                limit
            Return:
        """
        objetos = InfoBusquedaArticuloJumbo.objects.all()
        if 'id' in kwargs:
            objetos = objetos.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            objetos = objetos.filter(id__in=kwargs['ids'])

        if 'estado' in kwargs:
            objetos = objetos.filter(estado=kwargs['estado'])
        if 'estados' in kwargs:
            objetos = objetos.filter(estado__in=kwargs['estados'])

        if 'identificador_busqueda' in kwargs:
            objetos = objetos.filter(identificador_busqueda=kwargs['identificador_busqueda'])
        if 'identificadores_busqueda' in kwargs:
            objetos = objetos.filter(identificador_busqueda__in=kwargs['identificadores_busqueda'])
        if 'order_by' in kwargs:
            objetos = objetos.order_by(kwargs['order_by'])
        if 'limit' in kwargs:
            objetos = objetos[:kwargs['limit']]
        return objetos



    @staticmethod
    def crearInfoBusquedaArticuloJumbo(identificador_busqueda, estado, intentos=1, user_id=None):
        """
            Función que ingresa una nueva InfoBusquedaArticuloJumbo
            Param:
                <Char>identificador_busqueda
                <Char>estado: estado de la búsqueda puede ser ENCONTRADO, EN_PROCESO, NO_ENCONTRADO
            Return:
                InfoBusquedaArticuloJumbo
                None en caso de existir la InfoBusquedaArticuloJumbo en la base de datos
        """

        if len(ManagerArticuloJumbo.obtenerInfosBusquedaArticuloJumbo(identificador_busqueda=identificador_busqueda)) > 0:
            return None
        aux_infobusquedaarticulojumbo = InfoBusquedaArticuloJumbo(
            identificador_busqueda=identificador_busqueda,
            estado=estado,
            intentos=intentos,
        )
        aux_infobusquedaarticulojumbo.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloJumbo.supermercado,
            tipo=ManagerArticuloJumbo.clases['INFO_BUSQUEDA'],
            status='INFO',
            info= {'mensaje':'Agregado el identificador {} para búsqueda'.format(identificador_busqueda)},
            modelo_id=aux_infobusquedaarticulojumbo.id,
            user_id=user_id
        )
        return aux_infobusquedaarticulojumbo


    @staticmethod
    def actualizarInfoBusquedaArticuloJumbo(infobusquedaarticulojumbo, estado, intentos=None, agregar_intento=True, identificador_busqueda=None, user_id=None):
        """
            Función que ingresa o actualiza la info de actualizacion de un ArticuloJumbo
            Param:
                <int>(id_info) o <string>(identificador) o <InfoBusquedaArticuloJumbo>  infobusquedaarticulojumbo
                estado
                intentos
                identificador_busqueda
                user_id
            Return:
                InfoBusquedaArticuloJumbo
                None en caso de existir la info busqueda Jumbo en la base de datos
        """
        info_busqueda = None
        if type(infobusquedaarticulojumbo) == type(1):
            info_busqueda = ManagerArticuloJumbo.obtenerInfoBusquedaArticuloJumbo(infobusquedaarticulojumbo)
        elif type(infobusquedaarticulojumbo) == type('string'):
            infos_busqueda = ManagerArticuloJumbo.obtenerInfosBusquedaArticuloJumbo(identificador_busqueda=infobusquedaarticulojumbo)
            if infos_busqueda.count() > 0:
                info_busqueda = infos_busqueda[0]
        elif type(infobusquedaarticulojumbo) == type(InfoBusquedaArticuloJumbo()):
            info_busqueda = infobusquedaarticulojumbo
        if info_busqueda is None:
            return None
        info_busqueda.estado = estado
        if intentos is None:
            if agregar_intento:
                info_busqueda.intentos = info_busqueda.intentos + 1
        if identificador_busqueda is not None:
            info_busqueda.identificador_busqueda = identificador_busqueda
        info_busqueda.ultima_actualizacion = datetime.now()
        info_busqueda.save()
        return info_busqueda


    ################################################################
    ####       Promociones Jumbo
    #################################################################


    @staticmethod
    def obtenerPromocionJumbo(id):
        """
            Función que obtiene el PromocionJumbo según su id
            Param:
                id: id de la PromocionJumbo
            Return:
                PromocionJumbo
                None en caso de no existir el PromocionJumbo
        """
        try:
            return PromocionJumbo.objects.get(id=id)
        except Exception,e:
            return None

    @staticmethod
    def obtenerPromocionesJumbo(**kwargs):
        """
            Función para recuperar PromocionJumbo
            Params:
                
            Return:
        """
        items = PromocionJumbo.objects.all()
        if 'id' in kwargs:
            items = items.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            items = items.filter(id__in=kwargs['ids'])
        if 'promocion_id' in kwargs:
            items = items.filter(promocion_id=kwargs['promocion_id'])
        if 'promociones_id' in kwargs:
            items = items.filter(promocion_id__in=kwargs['promociones_id'])
        if 'estado' in kwargs:
            items = items.filter(estado=kwargs['estado'])
        if 'estados' in kwargs:
            items = items.filter(estados__in=kwargs['estados'])
        if 'order_by' in kwargs:
            items = items.order_by(kwargs['order_by'])
        if 'limit' in kwargs:
            items = items[:kwargs['limit']]
        return items






    @staticmethod 
    def crearPromocionJumbo(habilitada, promocion_id, nombre, grupo, tipo, tipo_descuento,
                        tipo_promocion, valor,fecha_inicio, fecha_final, dias_disponible,
                     cantidad, cantidad_afectada, estado, estado_mensaje, user_id=None):
        """
            Función que ingresa un nuevo PromocionJumbo
            Param:
                <Boolean>habilitada
                <Char>promocion_id        key del diccionario
                <Char>nombre              name
                <Char>grupo               grupo
                <Char>tipo                type
                <Char>tipo_descuento      discountType
                <Char>tipo_promocion      promotionType
                <Char>valor               value
                <Datetime>fecha_inicio        start
                <Datetime>fecha_final         end
                <JSON>dias_disponible     availableDays
                <Integer>cantidad            quantity
                <Integer>cantidad_afectada   quantityAffected
                <Char>estado
                <Char>estado_mensaje
            Return:
                PromocionJumbo
                None en caso de existir la PromocionJumbo en la base de datos
        """

        if len(ManagerArticuloJumbo.obtenerPromocionesJumbo(promocion_id=promocion_id)) > 0:
            return None


        aux_promocionjumbo = PromocionJumbo(
            habilitada = habilitada,
            promocion_id = promocion_id,
            nombre = nombre,
            grupo = grupo,
            tipo = tipo,
            tipo_descuento = tipo_descuento,
            tipo_promocion = tipo_promocion,
            valor = valor,
            fecha_inicio = fecha_inicio,
            fecha_final = fecha_final,
            dias_disponible = dias_disponible,
            cantidad = cantidad,
            cantidad_afectada = cantidad_afectada,
            estado = estado,
            estado_mensaje = estado_mensaje,
        )

        aux_promocionjumbo.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloJumbo.supermercado,
            tipo=ManagerArticuloJumbo.clases['PROMOCION'],
            status='INFO',
            info= {'mensaje':'Promoción {} [promocion_id] ingresada'.format(promocion_id)},
            modelo_id=aux_promocionjumbo.id,
            user_id=user_id
        )

        return aux_promocionjumbo


    @staticmethod 
    def editarPromocionJumbo(promocionjumbo, habilitada=None, promocion_id=None, nombre=None, grupo=None,
                tipo=None, tipo_descuento=None, tipo_promocion=None, valor=None,fecha_inicio=None,
                fecha_final=None, dias_disponible=None, cantidad=None, cantidad_afectada=None,
                estado=None, estado_mensaje=None, user_id=None):
        """
            Función EDITAR un PromocionJumbo
            Param:
                <Integer>(articulojumbo_id) o <Char>promocion_id o <PromocionJumbo>
                <Boolean>habilitada
                <Char>promocion_id        key del diccionario
                <Char>nombre              name
                <Char>grupo               grupo
                <Char>tipo                type
                <Char>tipo_descuento      discountType
                <Char>tipo_promocion      promotionType
                <Char>valor               value
                <Datetime>fecha_inicio        start
                <Datetime>fecha_final         end
                <JSON>dias_disponible     availableDays
                <Integer>cantidad            quantity
                <Integer>cantidad_afectada   quantityAffected
                <Char>estado
                <Char>estado_mensaje
            Return:
                PromocionJumbo
                None en caso de existir la promoción Jumbo en la base de datos
        """
        aux_promocionjumbo = None
        if type(promocionjumbo) == type(1):
            aux_promocionjumbo = ManagerArticuloJumbo.obtenerPromocionJumbo(promocionjumbo)
        elif type(promocionjumbo) == type('string'):
            aux_promocionesjumbo = ManagerArticuloJumbo.obtenerPromocionesJumbo(promocion_id=promocionjumbo)
            if aux_promocionesjumbo.count() > 0:
                aux_promocionjumbo = aux_promocionesjumbo[0]
        elif type(promocionjumbo) == type(PromocionJumbo()):
            aux_promocionjumbo = promocionjumbo
        promocionjumbo = aux_promocionjumbo
        if promocionjumbo is None:
            return None
        info = {}
        if habilitada is not None:
            if promocionjumbo.habilitada != habilitada:
                info['habilitada'] = promocionjumbo.habilitada+' -> '+habilitada
                promocionjumbo.habilitada = habilitada
        if promocion_id is not None:
            if promocionjumbo.promocion_id != promocion_id:
                info['promocion_id'] = promocionjumbo.promocion_id+' -> '+promocion_id
                promocionjumbo.promocion_id = promocion_id
        if nombre is not None:
            if promocionjumbo.nombre != nombre:
                info['nombre'] = promocionjumbo.nombre+' -> '+nombre
                promocionjumbo.nombre = nombre
        if grupo is not None:
            if promocionjumbo.grupo != grupo:
                info['grupo'] = promocionjumbo.grupo+' -> '+grupo
                promocionjumbo.grupo = grupo
        if tipo is not None:
            if promocionjumbo.tipo != tipo:
                info['tipo'] = promocionjumbo.tipo+' -> '+tipo
                promocionjumbo.tipo = tipo
        if tipo_descuento is not None:
            if promocionjumbo.tipo_descuento != tipo_descuento:
                info['tipo_descuento'] = promocionjumbo.tipo_descuento+' -> '+tipo_descuento
                promocionjumbo.tipo_descuento = tipo_descuento
        if tipo_promocion is not None:
            if promocionjumbo.tipo_promocion != tipo_promocion:
                info['tipo_promocion'] = promocionjumbo.tipo_promocion+' -> '+tipo_promocion
                promocionjumbo.tipo_promocion = tipo_promocion
        if valor is not None:
            if promocionjumbo.valor != valor:
                info['valor'] = promocionjumbo.valor+' -> '+valor
                promocionjumbo.valor = valor

        if fecha_inicio is not None:
            if promocionjumbo.fecha_inicio != fecha_inicio:
                info['fecha_inicio'] = unicode(promocionjumbo.fecha_inicio)+' -> '+unicode(fecha_inicio)
                promocionjumbo.fecha_inicio = fecha_inicio
        if fecha_final is not None:
            if promocionjumbo.fecha_final != fecha_final:
                info['fecha_final'] = unicode(promocionjumbo.fecha_final)+' -> '+unicode(fecha_final)
                promocionjumbo.fecha_final = fecha_final

        if dias_disponible is not None:
            if promocionjumbo.dias_disponible != dias_disponible:
                info['dias_disponible'] = unicode(promocionjumbo.dias_disponible)+' -> '+unicode(dias_disponible)
                promocionjumbo.dias_disponible = dias_disponible
        if cantidad is not None:
            if promocionjumbo.cantidad != cantidad:
                info['cantidad'] = unicode(promocionjumbo.cantidad)+' -> '+unicode(cantidad)
                promocionjumbo.cantidad = cantidad
        if cantidad_afectada is not None:
            if promocionjumbo.cantidad_afectada != cantidad_afectada:
                info['cantidad_afectada'] = unicode(promocionjumbo.cantidad_afectada)+' -> '+unicode(cantidad_afectada)
                promocionjumbo.cantidad_afectada = cantidad_afectada
        if estado is not None:
            if promocionjumbo.estado != estado:
                info['estado'] = promocionjumbo.estado+' -> '+estado
                promocionjumbo.estado = estado
        if estado_mensaje is not None:
            if promocionjumbo.estado_mensaje != estado_mensaje:
                info['estado_mensaje'] = promocionjumbo.estado_mensaje+' -> '+estado_mensaje
                promocionjumbo.estado_mensaje = estado_mensaje
        promocionjumbo.save()
        
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloJumbo.supermercado,
            tipo=ManagerArticuloJumbo.clases['PROMOCION'],
            status='INFO',
            info=info,
            user_id=user_id,
            modelo_id=promocionjumbo.id,
        )
        return promocionjumbo



    @staticmethod 
    def extraerDataPromocionJumboDesdeDiccionario(data):
        """
            Función para extraer los datos recogidos desde jumbo para las promociones
            Param:
                <String>(JSON) <Diccionario> data: la estructura del diccionario desbe ser la misma
                         que la descripcion de productos proporcionada por Jumbo
            Return:
                <Diccionario> Este va con el nombre de los campos según el modelo PromocionJumbo
                Excepto los campos habiltada, promocion_id, estado, estado_mensaje
        """
        if type(data) == type('string'):
            data = json.loads(data)
        nombre = None 
        if 'name' in data:
            if data['name']:
                nombre = data['name']
        grupo = None 
        if 'group' in data:
            if data['group']:
                grupo = data['group']
        tipo = None 
        if 'type' in data:
            if data['type']:
                tipo = data['type']
        tipo_descuento = None 
        if 'discountType' in data:
            if data['discountType']:
                tipo_descuento = data['discountType']
        tipo_promocion = None 
        if 'promotionType' in data:
            if data['promotionType']:
                tipo_promocion = data['promotionType']
        valor = None 
        if 'value' in data:
            if data['value']:
                valor = data['value']
        fecha_inicio = None
        if 'start' in data:
            if data['start']:
                fecha_inicio = data['start']
                try:
                    fecha_inicio = datetime.strptime(data['start'].replace("T", " "),"%Y-%m-%d %H,%M,%S")
                except Exception, e:
                    pass
        fecha_final = None
        if 'end' in data:
            if data['end']:
                try:
                    fecha_final = datetime.strptime(data['end'].replace("T", " "),"%Y-%m-%d %H,%M,%S")
                except Exception, e:
                    pass
        dias_disponible = None
        if 'availableDays' in data:
            if data['availableDays']:
                dias_disponible = data['availableDays']
        cantidad = None
        if 'quantity' in data:
            if data['quantity']:
                try:
                    cantidad = int(data['quantity'])
                except Exception, e:
                    pass
        cantidad_afectada = None
        if 'quantityAffected' in data:
            if data['quantityAffected']:
                try:
                    cantidad_afectada = int(data['quantityAffected'])
                except Exception, e:
                    pass
        retorno = {
            'nombre': nombre,
            'grupo' : grupo,
            'tipo' : tipo,
            'tipo_descuento' : tipo_descuento,
            'tipo_promocion' : tipo_promocion,
            'valor':valor,
            'fecha_inicio': fecha_inicio,
            'fecha_final' : fecha_final,
            'dias_disponible' : dias_disponible,
            'cantidad': cantidad,
            'cantidad_afectada': cantidad_afectada,
        }
        return retorno


    @staticmethod
    def crearPromocionJumboDesdeDiccionario(promocion_id, data, user_id=None):
        """
            Función que ingresa una nueva PromocionJumbo desde un diccionario, la estructura 
            del diccionario desbe ser la misma que la descripcion de productos proporcionada por Jumbo
            Param:
                <Char> promocion_id
                <string>  o <diccionario>(JSON con el formato de Jumbo)  data: 
            Return:
                PromocionJumbo
                None en caso de existir la Promoción Jumbo en la base de datos
        """
        if len(ManagerArticuloJumbo.obtenerPromocionesJumbo(promocion_id=promocion_id)) > 0:
            return None
        dic_promocionjumbo = None
        if type(data) == type({}) or type(data) == type(""):
            dic_promocionjumbo = ManagerArticuloJumbo.extraerDataPromocionJumboDesdeDiccionario(data)
        else:
            raise Exception ("El parámetro data no es de tipo diccionario o string ")
        estado = 'OK'
        estado_mensaje = 'Ingresada nueva promoción'
        nueva_promocion = ManagerArticuloJumbo.crearPromocionJumbo(
            habilitada=True,
            promocion_id=promocion_id,
            nombre=dic_promocionjumbo['nombre'],
            grupo=dic_promocionjumbo['grupo'],
            tipo=dic_promocionjumbo['tipo'],
            tipo_descuento=dic_promocionjumbo['tipo_descuento'],
            tipo_promocion=dic_promocionjumbo['tipo_promocion'],
            valor=dic_promocionjumbo['valor'],
            fecha_inicio=dic_promocionjumbo['fecha_inicio'],
            fecha_final=dic_promocionjumbo['fecha_final'],
            dias_disponible=dic_promocionjumbo['dias_disponible'],
            cantidad=dic_promocionjumbo['cantidad'],
            cantidad_afectada=dic_promocionjumbo['cantidad_afectada'],
            estado=estado,
            estado_mensaje=estado_mensaje,
            user_id=user_id
        )
        if nueva_promocion is None:
            ManagerLogSupermercado.crearLog(grupo=ManagerArticuloJumbo.supermercado, tipo=ManagerArticuloJumbo.clases['PROMOCION'], status='ERROR', info= {'mensaje':'La promoción {} [promocion_id] ya se encuentra ingresada'.format(promocion_id)} , user_id=user_id)
        return nueva_promocion




    @staticmethod
    def actualizarPromocionJumboDesdeDiccionario(promocion_id, data, user_id=None):
        """
            Función que actualiza una PromocionJumbo existente en la base de datos desde un diccionario, la estructura 
            del diccionario desbe ser la misma que la descripcion de productos proporcionada por Jumbo
            Param:
                <string> promocion_id
                <string>(JSON con el formato de Jumbo) o <diccionario> (Ya procesado) data: 
            Return:
                PromocionJumbo
                None en caso de no existir la promocion Jumbo en la base de datos
        """
        dic_promocionjumbo = None
        if type(data) == type({}) or type(data) == type(""):
            dic_promocionjumbo = ManagerArticuloJumbo.extraerDataPromocionJumboDesdeDiccionario(data)
        else:
            raise Exception ("El parámetro data no es de tipo diccionario o string ")


        estado = 'OK'
        estado_mensaje = 'Articulo actualizado'

        promocionjumbo= ManagerArticuloJumbo.editarPromocionJumbo(
            promocionjumbo=promocion_id,
            habilitada=True,
            promocion_id=promocion_id,
            nombre=dic_promocionjumbo['nombre'],
            grupo=dic_promocionjumbo['grupo'],
            tipo=dic_promocionjumbo['tipo'],
            tipo_descuento=dic_promocionjumbo['tipo_descuento'],
            tipo_promocion=dic_promocionjumbo['tipo_promocion'],
            valor=dic_promocionjumbo['valor'],
            fecha_inicio=dic_promocionjumbo['fecha_inicio'],
            fecha_final=dic_promocionjumbo['fecha_final'],
            dias_disponible=dic_promocionjumbo['dias_disponible'],
            cantidad=dic_promocionjumbo['cantidad'],
            cantidad_afectada=dic_promocionjumbo['cantidad_afectada'],
            estado=estado,
            estado_mensaje=estado_mensaje,
            user_id=user_id
        )

        if promocionjumbo is None:
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloJumbo.supermercado,
                tipo=ManagerArticuloJumbo.clases['PROMOCION'],
                status='ERROR',
                info= {'mensaje':'La promoción no existe'.format(promocionjumbo)},
                user_id=user_id
            )
