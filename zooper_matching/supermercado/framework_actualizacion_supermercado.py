# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from supermercado.jumbo.framework_actualizacion_jumbo import ManagerActualizacionJumbo
from supermercado.lider.framework_actualizacion_lider import ManagerActualizacionLider

class ManagerSupermercados():
    """
        Se encarga de la gestión de búsqueda y actualizacion de nuevos productos
    """

    @staticmethod
    def obtenerElementosAActualizar(supermercado):
        """
            Funcion que retorna las distintas url a trabajar por el cliente 
            param:
                (String) supermercado: identificador del supermercado a actualizar
            return:
                [] con urls a actualizar
                <Diccionario>
                    {
                        supermercado_1:[url_1,url_2],
                        supermercado_2:[url_1,url_2],
                    }
        """
        retorno = []
        if supermercado == 'jumbo':
            aux = ManagerActualizacionJumbo.obtenerURLArticulosAActualizar()
            if aux is not None:
                retorno.append(aux)
            aux = ManagerActualizacionJumbo.busquedaURLNuevosProductos()
            if aux is not None:
                retorno.append(aux)
        elif supermercado == 'lider':
            retorno = ManagerActualizacionLider.obtenerUrlsInfoBusquedaArticulosEnProceso()
        else:
            return None
        return retorno


    @staticmethod
    def ingresarResultadosPeticion(supermercado, data, opcion='ingreso_producto', lote=True, user_id=None):
        """
            Funcion para ingresar los resultados obtenidos por los usuarios
            param:
                supermercado: supermercado al que pertence los datos
                data: JSON con los datos en el formato entregado por el supermercado
                lote: especifica si el JSON trae 1 o varios productos a ingresar
                opcion: Opcion de ingreso según el supermercado
            return:
                None
        """
        print 'ingresarResultadosPeticion'
        retorno = {}
        if supermercado == "jumbo":
            if lote:
                ManagerActualizacionJumbo.ingresarArticuloJumboLote(data, user_id=user_id)
            else:
                ManagerActualizacionJumbo.ingresarArticuloJumbo(data, user_id=user_id)
        elif supermercado == "lider":
            if opcion == 'ingreso_busqueda':
                if type(data) == type({}):
                    data = data['url']
                ManagerActualizacionLider.ingresarInfoBusquedaArticuloLider(data)
            elif opcion == 'ingreso_producto':
                print 'ingreso_producto'
                ManagerActualizacionLider.ingresarArticuloLider(data)
