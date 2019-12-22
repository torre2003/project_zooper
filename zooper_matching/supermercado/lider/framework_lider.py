# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import pytz
utc=pytz.UTC

from datetime import datetime
from django.db import transaction

from models import ArticuloLider, InfoActualizacionArticuloLider, InfoBusquedaArticuloLider
from supermercado.framework_supermercado import ManagerLogSupermercado


class ManagerArticuloLider(object):
    """
        Clase para administrar los producto
    """
    clase = 'ArticuloLider'
    titulo = 'Supermercado Lider'
    supermercado = 'lider'
    clases = {
        'ARTICULO':'ArticuloLider',
        'INFO_ACTUALIZACION':'InfoActualizacionArticuloLider',
        'INFO_BUSQUEDA':'InfoBusquedaArticuloLider',
    }

    ####################################################################################
    ####################################################################################
    ###  Articulo Lider
    ####################################################################################
    ####################################################################################

    @staticmethod
    def obtenerArticulo(id):
        """
            Función que obtiene el ArticuloLider según su id
            Param:
                id: id del producto
            Return:
                ArticuloLider
                None en caso de no existir el ArticuloLider
        """
        try:
            return ArticuloLider.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtenerArticulos(**kwargs):
        """
            Función para recuperar ArticulosLider
            Params:
                
            Return:
        """
        articulo = ArticuloLider.objects.all()
        if 'id' in kwargs:
            articulo = articulo.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            articulo = articulo.filter(id__in=kwargs['ids'])

        if 'codigo' in kwargs:
            articulo = articulo.filter(codigo=kwargs['codigo'])
        if 'codigos' in kwargs:
            articulo = articulo.filter(codigo__in=kwargs['codigos'])

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
    def crearArticuloLider( codigo, nombre, marca, url_imagen, url_producto, caracteristica, precio_alto, precio_bajo, 
        precio_unidad_medida, etiquetas_precio, etiquetas_oferta, estado, estado_mensaje, user_id=None):
        """
            Función que ingresa un nuevo ArticuloLider
            Param:
                <Char>codigo
                <Char>nombre
                <Char>marca
                <Char>url_imagen
                <Char>url_producto
                <Char>caracteristica
                <Integer>precio_alto
                <Integer>precio_bajo
                <Char>precio_unidad_medida
                <JSON>etiquetas_precio
                <JSON>etiquetas_oferta
                <Char>estado
                <Char>estado_mensaje
            Return:
                ArticuloLider
                None en caso de existir el articulo Lider en la base de datos
        """
        if len(ManagerArticuloLider.obtenerArticulos(codigo=codigo)) > 0:
            return None
        if len(ManagerArticuloLider.obtenerArticulos(marca=marca, nombre=nombre)) > 0:
            return None
        if len(ManagerArticuloLider.obtenerArticulos(url_producto=url_producto)) > 0:
            return None

        aux_articulolider=ArticuloLider(
            codigo=codigo,
            nombre=nombre,
            marca=marca,
            url_imagen=url_imagen,
            url_producto=url_producto,
            caracteristica=caracteristica,
            precio_alto=precio_alto,
            precio_bajo=precio_bajo,
            precio_unidad_medida=precio_unidad_medida,
            etiquetas_precio=etiquetas_precio,
            etiquetas_oferta=etiquetas_oferta,
            estado=estado,
            estado_mensaje=estado_mensaje,
        )

        aux_articulolider.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloLider.supermercado,
            tipo=ManagerArticuloLider.clases['ARTICULO'],
            status='INFO',
            info= {'mensaje':'Producto {} [codigo] ingresado'.format(codigo)},
            modelo_id=aux_articulolider.id,
            user_id=user_id
        )
        ManagerArticuloLider.actualizarInfoActualizacionArticuloLider(aux_articulolider.id, estado='ACTUALIZADO', estado_mensaje='Creación articulo', user_id=user_id)
        return aux_articulolider

    @staticmethod
    def editarArticuloLider(articulolider, codigo=None, nombre=None, marca=None, url_imagen=None, url_producto=None,
            caracteristica=None, precio_alto=None, precio_bajo=None, precio_unidad_medida=None, etiquetas_precio=None,
            etiquetas_oferta=None, estado=None, estado_mensaje=None, user_id=None):

        """
            Función EDITAR un ArticuloLider
            Param:
                <Integer>(articulolider_id) o <Char>codigo o <ArticuloLider>
                <Char>codigo
                <Char>nombre
                <Char>marca
                <Char>url_imagen
                <Char>url_producto
                <Char>caracteristica
                <Integer>precio_alto
                <Integer>precio_bajo
                <Char>precio_unidad_medida
                <JSON>etiquetas_precio
                <JSON>etiquetas_oferta
                <Char>estado
                <Char>estado_mensaje
            Return:
                ArticuloLider
                None en caso de NO existir el articulo Lider en la base de datos
        """

        aux_articulolider = None
        if type(articulolider) == type(1):
            aux_articulolider = ManagerArticuloLider.obtenerArticulo(articulolider)
        elif type(articulolider) == type('string'):
            aux_articulolider = ManagerArticuloLider.obtenerArticulos(codigo=codigo)
            if aux_articulolider.count() > 0:
                aux_articulolider = aux_articulolider[0]
        elif type(articulolider) == type(ArticuloLider()):
            aux_articulolider = articulolider
        articulolider = aux_articulolider
        if articulolider is None:
            return None
        info = {}
        if codigo is not None:
            if articulolider.codigo != codigo:
                info['codigo'] = articulolider.codigo+' -> '+codigo
                articulolider.codigo = codigo
        if nombre is not None:
            if articulolider.nombre != nombre:
                info['nombre'] = articulolider.nombre+' -> '+nombre
                articulolider.nombre = nombre
        if marca is not None:
            if articulolider.marca != marca:
                info['marca'] = articulolider.marca+' -> '+marca
                articulolider.marca = marca
        if url_imagen is not None:
            if articulolider.url_imagen != url_imagen:
                info['url_imagen'] = articulolider.url_imagen+' -> '+url_imagen
                articulolider.url_imagen = url_imagen
        if url_producto is not None:
            if articulolider.url_producto != url_producto:
                info['url_producto'] = articulolider.url_producto+' -> '+url_producto
                articulolider.url_producto = url_producto
        if caracteristica is not None:
            if articulolider.caracteristica != caracteristica:
                info['caracteristica'] = articulolider.caracteristica+' -> '+caracteristica
                articulolider.caracteristica = caracteristica
        if precio_alto is not None:
            if articulolider.precio_alto != precio_alto:
                info['precio_alto'] = unicode(articulolider.precio_alto)+' -> '+unicode(precio_alto)
                articulolider.precio_alto = precio_alto
        if precio_bajo is not None:
            if articulolider.precio_bajo != precio_bajo:
                info['precio_bajo'] = unicode(articulolider.precio_bajo)+' -> '+unicode(precio_bajo)
                articulolider.precio_bajo = precio_bajo
        if precio_unidad_medida is not None:
            if articulolider.precio_unidad_medida != precio_unidad_medida:
                info['precio_unidad_medida'] = articulolider.precio_unidad_medida+' -> '+precio_unidad_medida
                articulolider.precio_unidad_medida = precio_unidad_medida
        if etiquetas_precio is not None:
            if articulolider.etiquetas_precio != etiquetas_precio:
                info['etiquetas_precio'] = unicode(articulolider.etiquetas_precio)+' -> '+unicode(etiquetas_precio)
                articulolider.etiquetas_precio = etiquetas_precio
        if etiquetas_oferta is not None:
            if articulolider.etiquetas_oferta != etiquetas_oferta:
                info['etiquetas_oferta'] = unicode(articulolider.etiquetas_oferta)+' -> '+unicode(etiquetas_oferta)
                articulolider.etiquetas_oferta = etiquetas_oferta
        if estado is not None:
            if articulolider.estado != estado:
                info['estado'] = articulolider.estado+' -> '+estado
                articulolider.estado = estado
        if estado_mensaje is not None:
            if articulolider.estado_mensaje != estado_mensaje:
                info['estado_mensaje'] = articulolider.estado_mensaje+' -> '+estado_mensaje
                articulolider.estado_mensaje = estado_mensaje
        articulolider.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloLider.supermercado,
            tipo=ManagerArticuloLider.clases['ARTICULO'],
            status='INFO',
            info=info,
            user_id=user_id,
            modelo_id=articulolider.id,
        )
        ManagerArticuloLider.actualizarInfoActualizacionArticuloLider(aux_articulolider.id, estado='ACTUALIZADO', estado_mensaje='', user_id=user_id)
        return articulolider


    @staticmethod
    def extraerDataArticuloLiderDesdeDiccionario(data):
        """
            Función para extraer los datos recogidos desde Lider
            Param:
                <String>(JSON) <Diccionario> data: la estructura del diccionario desbe ser la misma
                         que la descripcion de productos proporcionada por Scrapy en script productolider
            Return:
                <Diccionario> Este va con el nombre de los campos según el modelo ArticuloLider
        """
        if type(data) == type('string'):
            data = json.loads(data)
        codigo = None
        if 'codigo' in data:
            if data['codigo']:
                codigo = data['codigo']
        nombre = None
        if 'nombre' in data:
            if data['nombre']:
                nombre = data['nombre']
        marca = None
        if 'marca' in data:
            if data['marca']:
                marca = data['marca']
        url_imagen = None
        if 'url_imagen' in data:
            if data['url_imagen']:
                url_imagen = data['url_imagen']
        url_producto = None
        if 'url_producto' in data:
            if data['url_producto']:
                url_producto = data['url_producto']
        caracteristica = None
        if 'caracteristica' in data:
            if data['caracteristica']:
                caracteristica = data['caracteristica']
        precio_bajo = None
        precio_alto = None
        if 'precio' in data:
            if data['precio']:
                precio_bajo = int(data['precio'])
                precio_alto = int(data['precio'])
        precio_unidad_medida = None
        if 'precio_unidad_medida' in data:
            if data['precio_unidad_medida']:
                precio_unidad_medida = data['precio_unidad_medida']

        etiquetas_precio = {'lowPrice':None,'highPrice':None,'others':[]}
        if 'etiquetas_precio' in data:
            if type(data['etiquetas_precio']) == type([]):
                for item in data['etiquetas_precio']:
                    print 'i'*20
                    if item['itemprop'] == 'lowPrice':
                        print item
                        if item['content']:
                            precio_bajo = int(item['content'])
                            etiquetas_precio['lowPrice'] = item['content']
                    if item['itemprop'] == 'highPrice':
                        if item['content']:
                            precio_alto = int(item['content'])
                            etiquetas_precio['highPrice'] = item['content']
                    if item['itemprop'] == '':
                        if item['texto']:
                            etiquetas_precio['others'].append(item['texto'])
        etiquetas_oferta = {}
        if 'etiquetas_oferta' in data:
            if type(data['etiquetas_oferta']) == type([]):
                i = 0
                for item in data['etiquetas_oferta']:
                    etiquetas_oferta[i]={
                        'clase':item['clase'],
                        'otros':item['otros'],
                        'texto':item['texto'],
                    }
                    i = i +1 
        aux_producto = {
            'codigo':codigo,
            'nombre':nombre,
            'marca':marca,
            'url_imagen':url_imagen,
            'url_producto':url_producto,
            'caracteristica':caracteristica,
            'precio_alto':precio_alto,
            'precio_bajo':precio_bajo,
            'precio_unidad_medida':precio_unidad_medida,
            'etiquetas_precio':etiquetas_precio,
            'etiquetas_oferta':etiquetas_oferta
        }

        return aux_producto



    @staticmethod
    def crearArticuloLiderDesdeDiccionario(data, user_id=None):
        """
            Función que ingresa un nuevo ArticuloLider desde un diccionario, la estructura 
            del diccionario debe ser la misma que la proporcionada por Scrapy en lider_producto.py
            Param:
                <string>  o <diccionario>(JSON con el formato de Scrapy lider_producto.py)  data: 
            Return:
                ArticuloLider
                None en caso de existir el articulo Lider en la base de datos
        """
        print 'a.1'
        dic_articulolider = None
        print 'a.2'
        if type(data) == type({}) or type(data) == type(""):
            dic_articulolider = ManagerArticuloLider.extraerDataArticuloLiderDesdeDiccionario(data)
        else:
            raise Exception ("El parámetro data no es de tipo diccionario o string ")
        print 'a.3'
        estado = 'OK'
        estado_mensaje = 'Ingresado nuevo articulo'
        print 'a.4'
        nuevo_articulo = ManagerArticuloLider.crearArticuloLider(
            codigo=dic_articulolider['codigo'],
            nombre=dic_articulolider['nombre'],
            marca=dic_articulolider['marca'],
            url_imagen=dic_articulolider['url_imagen'],
            url_producto=dic_articulolider['url_producto'],
            caracteristica=dic_articulolider['caracteristica'],
            precio_alto=dic_articulolider['precio_alto'],
            precio_bajo=dic_articulolider['precio_bajo'],
            precio_unidad_medida=dic_articulolider['precio_unidad_medida'],
            etiquetas_precio=dic_articulolider['etiquetas_precio'],
            etiquetas_oferta=dic_articulolider['etiquetas_oferta'],
            estado=estado,
            estado_mensaje=estado_mensaje,
            user_id=user_id
        )
        print 'a.5'
        if nuevo_articulo is None:
            ManagerLogSupermercado.crearLog(grupo=ManagerArticuloLider.supermercado, tipo=ManagerArticuloLider.clase, status='ERROR', info= {'mensaje':'El producto {} [código] ya se encuentra ingresado'.format(dic_articulolider['codigo'])} , user_id=user_id)
        print 'a.6'
        return nuevo_articulo



    @staticmethod
    def actualizarArticuloLiderDesdeDiccionario(data, user_id=None):
        """
            Función que actualiza un ArticuloLider existente en la base de datos desde un diccionario, la estructura 
            del diccionario debe ser la misma que la proporcionada por Scrapy en lider_producto.py
            Param:
                <string>(JSON con el formato Scrapy en lider_producto.py) o <diccionario> (Ya procesado) data: 
            Return:
                ArticuloLider
                None en caso de no existir el articulo Lider en la base de datos
        """
        print 'b.1'
        dic_articulolider = None
        if type(data) == type({}) or type(data) == type(""):
            dic_articulolider = ManagerArticuloLider.extraerDataArticuloLiderDesdeDiccionario(data)
        else:
            raise Exception ("El parámetro data no es de tipo diccionario o string ")
        print 'b.2'
        estado = 'OK'
        estado_mensaje = 'Articulo actualizado'
        print 'b.3'
        articulolider = ManagerArticuloLider.editarArticuloLider(
            articulolider=dic_articulolider['codigo'],
            codigo=dic_articulolider['codigo'],
            nombre=dic_articulolider['nombre'],
            marca=dic_articulolider['marca'],
            url_imagen=dic_articulolider['url_imagen'],
            url_producto=dic_articulolider['url_producto'],
            caracteristica=dic_articulolider['caracteristica'],
            precio_alto=dic_articulolider['precio_alto'],
            precio_bajo=dic_articulolider['precio_bajo'],
            precio_unidad_medida=dic_articulolider['precio_unidad_medida'],
            etiquetas_precio=dic_articulolider['etiquetas_precio'],
            etiquetas_oferta=dic_articulolider['etiquetas_oferta'],
            estado=estado,
            estado_mensaje=estado_mensaje,
            user_id=user_id
        )

        print 'b.4'
        if articulolider is None:
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloLider.supermercado,
                tipo=ManagerArticuloLider.clases['ARTICULO'],
                status='ERROR',
                info= {'mensaje':'El producto no existe {} [Código]'.format(dic_articulolider['codigo'])},
                user_id=user_id
            )
        print 'b.5'
        return articulolider

    ####################################################################################
    ####################################################################################
    ###  Info Actualización Articulo Lider
    ####################################################################################
    ####################################################################################

    @staticmethod
    def obtenerInfoActualizacionArticuloLider(id):
        """
            Función que obtiene el InfoActualizacionArticuloLider según su id
            Param:
                id: id del producto
            Return:
                InfoActualizacionArticuloLider
                None en caso de no existir el InfoActualizacionArticuloLider
        """
        try:
            return InfoActualizacionArticuloLider.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtenerInfosActualizacionArticuloLider(**kwargs):
        """
            Función para recuperar InfoActualizacionArticuloLider
            Params:
                id
                ids
                articulolider_id
                articulolider_ids
                estado
                estados
                limit
            Return:
        """
        infosactualizacionarticulolider = InfoActualizacionArticuloLider.objects.all()
        if 'id' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.filter(id__in=kwargs['ids'])

        if 'articulolider_id' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.filter(articulolider_id=kwargs['articulolider_id'])
        if 'articulolider_ids' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.filter(articulolider_id__in=kwargs['articulolider_ids'])

        if 'estado' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.filter(estado=kwargs['estado'])
        if 'estados' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.filter(estado__in=kwargs['estados'])
        if 'order_by' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider.order_by(kwargs['order_by'])
        if 'limit' in kwargs:
            infosactualizacionarticulolider = infosactualizacionarticulolider[:kwargs['limit']]
        return infosactualizacionarticulolider


    @staticmethod
    def actualizarInfoActualizacionArticuloLider(articulolider, estado, estado_mensaje, actualizar_fecha=True,
                                                url_actualizacion=None, user_id=None):
        """
            Función que ingresa o actualiza la info de actualizacion de un ArticuloLider
            Param:
                <Integer> o <ArticuloLider> o <InfoActualizacionArticuloLider> articulolider
                <Char>estado   NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
                estado_mensaje
                actualizar_fecha
                url_actualizacion
                user_id
            Return:
                InfoActualizacionArticuloLider
                None en caso de existir el articulo Lider en la base de datos
        """
        info_actualizacion = None
        if type(articulolider) == type(1) or type(articulolider) == type(ArticuloLider()):
            if type(articulolider) == type(1):
                articulolider = ManagerArticuloLider.obtenerArticulo(articulolider)
            info_actualizacion =  ManagerArticuloLider.obtenerInfosActualizacionArticuloLider(articulolider_id=articulolider.id)
            if info_actualizacion.count() == 0:
                url_actualizacion = articulolider.url_producto
                info_actualizacion = InfoActualizacionArticuloLider(
                    articulolider=articulolider,
                    url_actualizacion=url_actualizacion,
                    estado=estado,
                    estado_mensaje=estado_mensaje,
                )
                info_actualizacion.save()
                return info_actualizacion
            else:
                info_actualizacion = info_actualizacion[0]
        elif type(articulolider) == type(InfoActualizacionArticuloLider()):
            info_actualizacion = articulolider
        else:
            raise Exception('Tipo no corresponde')
        if articulolider is None:
            return None
        info_actualizacion.estado = estado
        info_actualizacion.estado_mensaje = estado_mensaje
        if actualizar_fecha:
            info_actualizacion.ultima_actualizacion = datetime.now()
        info_actualizacion.save()
        return info_actualizacion

    ####################################################################################
    #####################################################
    ####  Info Busqueda Articulo Lider
    #####################################################
    ####################################################################################

    @staticmethod
    def obtenerInfoBusquedaArticuloLider(id):
        """
            Función que obtiene el InfoBusquedaArticuloLider según su id
            Param:
                id: id de la busqueda
            Return:
                InfoBusquedaArticuloLider
                None en caso de no existir el InfoBusquedaArticuloLider
        """
        try:
            return InfoBusquedaArticuloLider.objects.get(id=id)
        except Exception,e:
            return None



    @staticmethod
    def obtenerInfosBusquedaArticuloLider(**kwargs):
        """
            Función para recuperar InfoBusquedaArticuloLider
            Params:
                id
                ids
                estado
                estados
                url_busqueda
                urls_busqueda
                limit
            Return:
        """
        objetos = InfoBusquedaArticuloLider.objects.all()
        if 'id' in kwargs:
            objetos = objetos.filter(id=kwargs['id'])
        if 'ids' in kwargs:
            objetos = objetos.filter(id__in=kwargs['ids'])

        if 'estado' in kwargs:
            objetos = objetos.filter(estado=kwargs['estado'])
        if 'estados' in kwargs:
            objetos = objetos.filter(estado__in=kwargs['estados'])

        if 'url_busqueda' in kwargs:
            objetos = objetos.filter(url_busqueda=kwargs['url_busqueda'])
        if 'urls_busqueda' in kwargs:
            objetos = objetos.filter(url_busqueda__in=kwargs['urls_busqueda'])

        if 'order_by' in kwargs:
            objetos = objetos.order_by(kwargs['order_by'])
        if 'limit' in kwargs:
            objetos = objetos[:kwargs['limit']]
        return objetos



    @staticmethod
    def crearInfoBusquedaArticuloLider(url_busqueda, estado, intentos=1, user_id=None):
        """
            Función que ingresa una nueva InfoBusquedaArticuloLider
            Param:
                <Char>url_busqueda
                <Char>estado: estado de la búsqueda puede ser ENCONTRADO, EN_PROCESO, NO_ENCONTRADO
            Return:
                InfoBusquedaArticuloLider
                None en caso de existir la InfoBusquedaArticuloLider en la base de datos
        """

        if len(ManagerArticuloLider.obtenerInfosBusquedaArticuloLider(url_busqueda=url_busqueda)) > 0:
            return None
        aux_infobusquedaarticulolider = InfoBusquedaArticuloLider(
            url_busqueda=url_busqueda,
            estado=estado,
            intentos=intentos,
        )
        aux_infobusquedaarticulolider.save()
        ManagerLogSupermercado.crearLog(
            grupo=ManagerArticuloLider.supermercado,
            tipo=ManagerArticuloLider.clases['INFO_BUSQUEDA'],
            status='INFO',
            info= {'mensaje':'Agregada la url {} para búsqueda'.format(url_busqueda)},
            modelo_id=aux_infobusquedaarticulolider.id,
            user_id=user_id
        )
        return aux_infobusquedaarticulolider


    @staticmethod
    def actualizarInfoBusquedaArticuloLider(infobusquedaarticulolider, estado, intentos=None, agregar_intento=True, url_busqueda=None, user_id=None):
        """
            Función que ingresa o actualiza la info de actualizacion de un ArticuloLider
            Param:
                <int>(id_info) o <string>(url_busqueda) o <InfoBusquedaArticuloLider>  infobusquedaarticulolider
                estado
                intentos
                url_busqueda
                user_id
            Return:
                InfoBusquedaArticuloLider
                None en caso de existir la info busqueda Lider en la base de datos
        """
        info_busqueda = None
        if type(infobusquedaarticulolider) == type(1):
            info_busqueda = ManagerArticuloLider.obtenerInfoBusquedaArticuloLider(infobusquedaarticulolider)
        elif type(infobusquedaarticulolider) == type('string'):
            infos_busqueda = ManagerArticuloLider.obtenerInfosBusquedaArticuloLider(url_busqueda=infobusquedaarticulolider)
            if infos_busqueda.count() > 0:
                info_busqueda = infos_busqueda[0]
        elif type(infobusquedaarticulolider) == type(InfoBusquedaArticuloLider()):
            info_busqueda = infobusquedaarticulolider
        if info_busqueda is None:
            return None
        info_busqueda.estado = estado
        if intentos is None:
            if agregar_intento:
                info_busqueda.intentos = info_busqueda.intentos + 1
        if url_busqueda is not None:
            info_busqueda.url_busqueda = url_busqueda
        info_busqueda.ultima_actualizacion = datetime.now()
        info_busqueda.save()
        return info_busqueda

