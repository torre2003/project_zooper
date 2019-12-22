# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import datetime, timedelta
from supermercado.jumbo.framework_jumbo import ManagerArticuloJumbo
from supermercado.framework_supermercado import ManagerConfiguracionSupermercado, ManagerLogSupermercado


class ManagerActualizacionJumbo(object):
    # ejemplo 'fq=productId%3A7203'
    @staticmethod
    def encolarArticulos(dias=0, horas=0, minutos=0, segundos=0, estados=['ACTUALIZADO']):
        """
            Función que marca los articulos como no actualizados
            Param:
                dias   = Espacio de tiempo en DIAS que se deben actualizar los registros
                horas   = Espacio de tiempo en HORAS que se deben actualizar los registros
                minutos   = Espacio de tiempo en MINUTOS que se deben actualizar los registros
                segundos   = Espacio de tiempo en SEGUNDOS que se deben actualizar los registros
                estados     = NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
            Return:
                None
        """

        delta = datetime.now() - timedelta(days=dias, hours=horas, minutes=minutos, seconds=segundos)
        infoactualizaciones = ManagerArticuloJumbo.obtenerInfosActualizacionArticuloJumbo(estados=estados).filter(
            ultima_actualizacion__lte=delta
        )
        for infoactualizacion in infoactualizaciones:
            ManagerArticuloJumbo.actualizarInfoActualizacionArticuloJumbo(
                articulojumbo=infoactualizacion,
                estado='NO_ACTUALIZADO', 
                estado_mensaje="falta actualización",
                actualizar_fecha=False
            )


    @staticmethod
    def obtenerURLArticulosAActualizar(url_unica=True, limit=50, estados=['NO_ACTUALIZADO']):
        """
            Función para obtener la o las url para actualizar los productos
            Param:
                <Bool>url_unica = Si esta marcada se retorna una sola URL para la extraccion de los producto,
                                    En caso contrario se devuelve una URL por producto
                <Integer>limit = cantidad de productos a retornar en la url, jumbo acepta maximo 50 por petición
                <Array>estados = NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
            Return:
                <String> URL consulta de productos
                o
                <Array> URLS productos
                o 
                None si no hay articulos a actualizar
        """
        infoactualizaciones = ManagerActualizacionJumbo\
            .obtenerArticulosAActualizar(estados=estados, limit=limit)
        identificadores = []
        for infoactualizacion in infoactualizaciones:
            identificadores.append(infoactualizacion.url_actualizacion)
            ManagerArticuloJumbo.actualizarInfoActualizacionArticuloJumbo(
                articulojumbo=infoactualizacion,
                estado='PENDIENTE_ACTUALIZACION',
                estado_mensaje="en actualización",
                actualizar_fecha=False
            )
        if len(identificadores) == 0:
            return None
        return ManagerActualizacionJumbo.generarURLArticulos(identificadores=identificadores, url_unica=url_unica)


    @staticmethod
    def obtenerArticulosAActualizar(limit=50, estados=['NO_ACTUALIZADO'], con_detalle=False):
        """
            Función para obtener la o las url para actualizar los productos
            Param:
                <Integer>limit = cantidad de productos a retornar en la url, jumbo acepta maximo 50 por petición
                <Array>estados = NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
            Return:
                <InfosActualizacionArticuloJumbo> Array
        """
        infoactualizaciones = ManagerArticuloJumbo.obtenerInfosActualizacionArticuloJumbo(estados=estados, limit=limit, order_by='ultima_actualizacion')
        if con_detalle:
            infoactualizaciones.select_related('articulojumbo')
        return infoactualizaciones

    @staticmethod
    def busquedaURLNuevosProductos(url_unica=True, user_id=None):
        """
            Función para gestionar la busqueda de nuevos productos
            su variable de gestión es jumbo_ids_actualizacion y es un json de la siguiente ManagerArticuloJumbo
            Params
                user_id
            Return
                <array> identificadores para la búsqueda de nuevos productos
                o
                None 
        """
        identificadores = ManagerActualizacionJumbo.busquedaNuevosProductos(user_id=user_id)
        if identificadores is not None:
            if len(identificadores) == 0:
                return None
        return ManagerActualizacionJumbo.generarURLArticulos(identificadores=identificadores, url_unica=url_unica)



    @staticmethod
    def busquedaNuevosProductos(user_id=None):
        """
            Función para gestionar la busqueda de nuevos productos
            su variable de gestión es jumbo_ids_actualizacion y es un json de la siguiente ManagerArticuloJumbo
            Params
                user_id
            Return
                <array> identificadores para la búsqueda de nuevos productos 
                None si no hay productos a buscar
        """
        limite_busqueda = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_limite_busqueda')[0].valor
        ultima_id_consultada = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_ultima_id_consultada')[0].valor
        ultima_id_ingresada = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_ultima_id_ingresada')[0].valor
        rango_busqueda = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_rango_busqueda')[0].valor
        maximo_intentos_busqueda = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_maximo_intentos_busqueda')[0].valor

        retorno = []
        if ultima_id_consultada - ultima_id_ingresada > rango_busqueda:
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloJumbo.supermercado,
                tipo=ManagerArticuloJumbo.clases['INFO_BUSQUEDA'],
                status='ALERTA',
                info= {
                    'mensaje':'Se ha llegado al límite de busqueda de nuevos productos [{}]'.format(rango_busqueda),
                    'ultima_id_ingresada':ultima_id_ingresada,
                    'ultima_id_consultada':ultima_id_consultada,
                },
                modelo_id=None,
                user_id=None
            )
            retorno = ManagerActualizacionJumbo._obtenerIdentificadorInfoBusquedaArticulosEnProceso(limit=limite_busqueda)
            if len(retorno) == 0:
                ManagerLogSupermercado.crearLog(
                    grupo=ManagerArticuloJumbo.supermercado,
                    tipo=ManagerArticuloJumbo.clases['INFO_BUSQUEDA'],
                    status='ALERTA',
                    info= {
                        'mensaje':'No hay elementos para actualizar, revisar el rango y maximo de intentos búsqueda',
                        'ultima_id_ingresada':ultima_id_ingresada,
                        'ultima_id_consultada':ultima_id_consultada,
                    },
                    modelo_id=None,
                    user_id=None
                )
                return None
        else:
            infonuevosarticulos = ManagerActualizacionJumbo._obtenerIdentificadorInfoBusquedaArticulosNuevos(limit=limite_busqueda, user_id=user_id)
            en_proceso = limite_busqueda - len(infonuevosarticulos)
            infoenprocesoarticulos = ManagerActualizacionJumbo._obtenerIdentificadorInfoBusquedaArticulosEnProceso(limit=en_proceso)
            for item in infonuevosarticulos:
                retorno.append(item)
            for item in infoenprocesoarticulos:
                retorno.append(item)
        return retorno


    @staticmethod
    def _obtenerIdentificadorInfoBusquedaArticulosEnProceso(limit=50):
        retorno = []
        maximo_intentos_busqueda = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_maximo_intentos_busqueda')[0].valor
        infos = ManagerArticuloJumbo.obtenerInfosBusquedaArticuloJumbo(estado='EN_PROCESO').filter(
            intentos__lte=maximo_intentos_busqueda,
        ).order_by(
            'intentos',
            'id'
        )
        i = 0
        while i < limit and i < infos.count(): 
            if infos[i].intentos == maximo_intentos_busqueda:
                info = ManagerArticuloJumbo.actualizarInfoBusquedaArticuloJumbo(infobusquedaarticulojumbo=infos[i],estado='NO_ENCONTRADO',agregar_intento=False)
            else:
                retorno.append(infos[i].identificador_busqueda)
                info = ManagerArticuloJumbo.actualizarInfoBusquedaArticuloJumbo(infobusquedaarticulojumbo=infos[i],estado='EN_PROCESO')
            i= i+1
        return retorno


    @staticmethod
    def _obtenerIdentificadorInfoBusquedaArticulosNuevos(limit=50, user_id=None):
        retorno = []
        configuracion_ultima_id_consultada = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_ultima_id_consultada')[0]
        ultima_id_consultada = configuracion_ultima_id_consultada.valor
        i = 0
        while i < limit:
            ultima_id_consultada = ultima_id_consultada + 1
            infobusqueda = ManagerArticuloJumbo.crearInfoBusquedaArticuloJumbo(
                identificador_busqueda=unicode(ultima_id_consultada),
                estado='EN_PROCESO',
                user_id=user_id
            )
            retorno.append(infobusqueda.identificador_busqueda)
            ManagerConfiguracionSupermercado.actualizarConfiguracionSupermercado(
                configuracionsupermercado=configuracion_ultima_id_consultada,
                valor=ultima_id_consultada,
            )
            i = i+1
        return retorno


    @staticmethod
    def generarURLArticulos(identificadores, url_unica=True):
        url_base = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_url_base')[0].valor
        url_base_field_query = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='jumbo_url_base_field_query')[0].valor
        retorno = url_base
        if not url_unica:
            retorno = []
        for item in identificadores:
            if url_unica:
                retorno = retorno + url_base_field_query + unicode(item)
            else:
                retorno.append( url_base + url_base_field_query + unicode(item) )
        return retorno


    @staticmethod
    def ingresarArticuloJumboLote(data, user_id=None):
        """
            Función para ingresar un lote de articulosJumbo desde una busqueda con varios elementos
            params:
                <JSON> data: con vario elementos de jumbo
            Return:
                None
        """
        if data is not None:
            if data:
                data = json.loads(data)
                for item in data:
                    print item['productId']
                    ManagerActualizacionJumbo.ingresarArticuloJumbo(data=item, user_id=user_id)


    @staticmethod
    def ingresarArticuloJumbo(data, user_id=None):
        """
            Función para ingresar o actualizar la información de un articulos de jumbo
            
            Params
                <JSON> o <DICCIONARIO> data: con formato de Jumbo
                user_id
            Return
                ArticuloJumbo
        """
        try:
            if type(data) == type("string"):
                data = json.loads(data)
            elif type(data) == type({}):
                pass
            else:
                return
            producto_id = data['productId']
            infos_busqueda = ManagerArticuloJumbo.obtenerInfosBusquedaArticuloJumbo(
                identificador_busqueda=producto_id,
                estados=['EN_PROCESO', 'NO_ENCONTRADO'],
            )
            if infos_busqueda.count() > 0:
                info_busqueda = infos_busqueda[0]
                ManagerArticuloJumbo.actualizarInfoBusquedaArticuloJumbo(
                    infobusquedaarticulojumbo=infos_busqueda[0],
                    estado='ENCONTRADO',
                    agregar_intento=False,
                    user_id=user_id
                )
                ManagerLogSupermercado.crearLog(
                    grupo=ManagerArticuloJumbo.supermercado,
                    tipo=ManagerArticuloJumbo.clases['INFO_BUSQUEDA'],
                    status='INFO',
                    info= {
                        'mensaje':'ArticuloJumbo encontrado {} '.format(producto_id),
                    },
                    modelo_id=info_busqueda.id,
                    user_id=user_id
                )
            articulojumbo = ManagerArticuloJumbo.obtenerArticulos(producto_id=producto_id)
            if articulojumbo.count()>0:
                articulojumbo = articulojumbo[0]
                ManagerArticuloJumbo.actualizarArticuloJumboDesdeDiccionario(data=data, user_id=user_id)
            else:
                articulojumbo = None
                ManagerArticuloJumbo.crearArticuloJumboDesdeDiccionario(data=data, user_id=user_id)
            ManagerConfiguracionSupermercado.actualizarConfiguracionSupermercado('jumbo_ultima_id_ingresada', valor=int(producto_id))
        except Exception, e:
            error= None 
            error_producto_id = None
            try:
                error = data['items'][0]['sellers'][0]['commertialOffer']['GetInfoErrorMessage']
                error_producto_id = producto_id
            except Exception, e:
                pass
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloJumbo.supermercado,
                tipo=ManagerArticuloJumbo.clases['ARTICULO'],
                status='ERROR',
                info= {
                    'mensaje':unicode(e),
                    'data':unicode(data),
                    'error_supemercado':error,
                    'producto_id':error_producto_id,
                },
                modelo_id=None,
                user_id=user_id
            )


    @staticmethod
    def ingresarPromocionJumbo(promocion_id, data, user_id=None):
        """
            Función para ingresar o actualizar la información de una promoción de jumbo
            
            Params
                id de la promoción
                <JSON> o <DICCIONARIO> data: con formato de Jumbo
                user_id
            Return
                PromocionJumbo
        """
        promocionjumbo = None
        try:
            if type(data) == type("string"):
                data = json.loads(data)
            elif type(data) == type({}):
                pass
            else:
                return
            promocionjumbo = ManagerArticuloJumbo.obtenerPromocionesJumbo(promocion_id=promocion_id)
            if promocionjumbo.count()>0:
                promocionjumbo = promocionjumbo[0]
                ManagerArticuloJumbo.actualizarPromocionJumboDesdeDiccionario(promocion_id=promocion_id, data=data, user_id=user_id)
            else:
                promocionjumbo = ManagerArticuloJumbo.crearPromocionJumboDesdeDiccionario(promocion_id=promocion_id, data=data, user_id=user_id)
        except Exception, e:
            print e
            error= 'No se pudo obtener el string de la excepción'
            try:
                error = unicode(e) 
            except Exception, e:
                pass
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloJumbo.supermercado,
                tipo=ManagerArticuloJumbo.clases['PROMOCION'],
                status='ERROR',
                info= {
                    'mensaje':error,
                    'data':unicode(data),
                    'promocion_id':promocion_id,
                },
                modelo_id=None,
                user_id=user_id
            )
        return promocionjumbo


    @staticmethod
    def ingresarPromocionJumboLote(data, marcar_como_deshabilitada=True, user_id=None):
        """
            Función para ingresar un lote de PromocionJumbo desde una busqueda con varios elementos
            params:
                <JSON> data: con varias promociones Jumbo
            Return:
                None
        """
        promos = ManagerArticuloJumbo.obtenerPromocionesJumbo()
        promos.update(habilitada=False)
        if data is not None:
            if data:
                data = json.loads(data)
                for promocion_id in data["value"]:
                    print promocion_id
                    ManagerActualizacionJumbo.ingresarPromocionJumbo(promocion_id=promocion_id, data=data["value"][promocion_id], user_id=user_id)

