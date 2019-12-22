# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import datetime, timedelta
from supermercado.lider.framework_lider import ManagerArticuloLider
from supermercado.framework_supermercado import ManagerConfiguracionSupermercado, ManagerLogSupermercado


class ManagerActualizacionLider(object):

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
        infoactualizaciones = ManagerArticuloLider.obtenerInfosActualizacionArticuloLider(estados=estados).filter(
            ultima_actualizacion__lte=delta
        )
        for infoactualizacion in infoactualizaciones:
            ManagerArticuloLider.actualizarInfoActualizacionArticuloLider(
                articulolider=infoactualizacion,
                estado='NO_ACTUALIZADO', 
                estado_mensaje="falta actualización",
                actualizar_fecha=False
            )


    @staticmethod
    def obtenerURLArticulosAActualizar(limit=50, estados=['NO_ACTUALIZADO']):
        """
            Función para obtener la o las url para actualizar los productos
            Param:
                <Integer>limit = cantidad de productos a retornar en la url, jumbo acepta maximo 50 por petición
                <Array>estados = NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
            Return:
                <Array> URLS productos
        """
        infoactualizaciones = ManagerActualizacionLider\
            .obtenerArticulosAActualizar(estados=estados, limit=limit)
        
        urls = []
        for urls in infoactualizaciones:
            urls.append(infoactualizacion.url_actualizacion)
            ManagerArticuloLider.actualizarInfoActualizacionArticuloJumbo(
                articulolider=infoactualizacion,
                estado='PENDIENTE_ACTUALIZACION',
                estado_mensaje="en actualización",
                actualizar_fecha=False
            )
        return urls


    @staticmethod
    def obtenerArticulosAActualizar(limit=50, estados=['NO_ACTUALIZADO'], con_detalle=False):
        """
            Función para obtener la o las url para actualizar los productos
            Param:
                <Integer>limit = cantidad de productos a retornar en la url
                <Array>estados = NO_ACTUALIZADO, ACTUALIZADO, PENDIENTE_ACTUALIZACION, ERROR
            Return:
                <InfosActualizacionArticuloLider> Array
        """
        infoactualizaciones = ManagerArticuloLider.obtenerInfosActualizacionArticuloLider(
            estados=estados,
            limit=limit,
            order_by='ultima_actualizacion'
        )
        if con_detalle:
            infoactualizaciones.select_related('articulolider')
        return infoactualizaciones



    @staticmethod
    def ingresarArticuloLider(data, user_id=None):
        """
            Función para ingresar o actualizar la información de un articulos de lider
            
            Params
                <JSON> o <DICCIONARIO> data: con formato de Lider
                user_id
            Return
                ArticuloLider
        """
        try:
            print 'ingresarArticuloLider'
            if type(data) == type("string"):
                data = json.loads(data)
            elif type(data) == type({}):
                pass
            else:
                return
            print '1'
            codigo = data['codigo']
            print '2'
            url_producto = data['url_producto']
            print '3'
            print 'https://www.lider.cl/supermercado/product/Drive-Detergente-Líquido-Perfect-Results-Recarga/660114'
            print url_producto
            _url_productos = url_producto.split('/')
            codigo = _url_productos[len(_url_productos)-1]
            infos_busqueda = ManagerArticuloLider.obtenerInfosBusquedaArticuloLider(
                # url_busqueda=url_producto,
                estados=['EN_PROCESO', 'NO_ENCONTRADO'],
            )
            infos_busqueda = infos_busqueda.filter(
                url_busqueda__icontains=codigo
            )
            print '4'
            if infos_busqueda.count() > 0:
                info_busqueda = infos_busqueda[0]
                print 'info_busqueda = infos_busqueda[0]'
                print info_busqueda
                ManagerArticuloLider.actualizarInfoBusquedaArticuloLider(
                    infobusquedaarticulolider=infos_busqueda[0],
                    estado='ENCONTRADO',
                    agregar_intento=False,
                    user_id=user_id
                )
                ManagerLogSupermercado.crearLog(
                    grupo=ManagerArticuloLider.supermercado,
                    tipo=ManagerArticuloLider.clases['INFO_BUSQUEDA'],
                    status='INFO',
                    info= {
                        'mensaje':'ArticuloLider encontrado {} [Código]'.format(codigo),
                    },
                    modelo_id=info_busqueda.id,
                    user_id=user_id
                )
            print '5'
            articulolider = ManagerArticuloLider.obtenerArticulos(codigo=codigo)
            print '6'
            if articulolider.count()>0:
                print '6.1'
                articulolider = articulolider[0]
                print '6.2'
                ManagerArticuloLider.actualizarArticuloLiderDesdeDiccionario(data=data, user_id=user_id)
            else:
                print '6.1.1'
                articulolider = None
                print '6.1.2'
                ManagerArticuloLider.crearArticuloLiderDesdeDiccionario(data=data, user_id=user_id)
            print '7'
            # ManagerConfiguracionSupermercado.actualizarConfiguracionSupermercado('lider_ultima_id_ingresada', valor=int(producto_id))
        except Exception, e:
            print 'Exception ingresarArticuloLider'
            print e
            error= None 
            error_codigo = None
            try:
                error = data['url_producto']
                error_codigo = data['codigo']
            except Exception, e:
                pass
            ManagerLogSupermercado.crearLog(
                grupo=ManagerArticuloLider.supermercado,
                tipo=ManagerArticuloLider.clases['ARTICULO'],
                status='ERROR',
                info= {
                    'mensaje':unicode(e),
                    'data':unicode(data),
                    'error_supemercado':error,
                    'error_codigo':error_codigo,
                },
                modelo_id=None,
                user_id=user_id
            )


    @staticmethod
    def ingresarInfoBusquedaArticuloLider(url_busqueda, user_id=None):
        """
            Función para ingresar una url de búsqueda para los articulos de lider
            
            Params
                url_busqueda
                user_id
            Return
                None
        """
        infos_busqueda = ManagerArticuloLider.obtenerInfosBusquedaArticuloLider(url_busqueda=url_busqueda)
        if infos_busqueda.count() == 0:
            infobusqueda = ManagerArticuloLider.crearInfoBusquedaArticuloLider(
                url_busqueda=url_busqueda,
                estado='EN_PROCESO',
                user_id=user_id
            )


    @staticmethod
    def obtenerUrlsInfoBusquedaArticulosEnProceso():
        """
            Función que obtiene los objetos infoBusquedaArticuloLider y actualiza la cantidad de intentos
            Params.
            Return:
                [] con urls de busqueda
        """
        retorno = []
        maximo_intentos_busqueda = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='lider_maximo_intentos_busqueda')[0].valor
        limite_busqueda = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre='lider_limite_busqueda')[0].valor
        infos = ManagerArticuloLider.obtenerInfosBusquedaArticuloLider(estado='EN_PROCESO').filter(
            intentos__lte=maximo_intentos_busqueda,
        ).order_by(
            'intentos',
            'id'
        )

        i = 0
        while i < limite_busqueda and i < infos.count(): 
            if infos[i].intentos == maximo_intentos_busqueda:
                info = ManagerArticuloLider.actualizarInfoBusquedaArticuloLider(infobusquedaarticulolider=infos[i],estado='NO_ENCONTRADO',agregar_intento=False)
            else:
                retorno.append(infos[i].url_busqueda)
                info = ManagerArticuloLider.actualizarInfoBusquedaArticuloLider(infobusquedaarticulolider=infos[i],estado='EN_PROCESO')
            i= i+1
        return retorno