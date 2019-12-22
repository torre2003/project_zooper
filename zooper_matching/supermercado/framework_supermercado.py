# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import LogSupermercado, ConfiguracionSupermercado
#from supermercado.jumbo.framework_actualizacion_jumbo import ManagerActualizacionJumbo


class ManagerLogSupermercado():
    ALERTA = 'ALERTA'
    ERROR = 'ERROR'
    INFO = 'INFO'

    @staticmethod
    def crearLog(grupo, tipo, status, info, modelo_id=None, user_id=None):
        """
            Función para crear un log de Cliente o PotencialCliente
            Params:
                user_id: id del usuario asociado al registro
                grupo: indentificado de grupo usualmente el supermercado
                tipo: identificado de modelo asociado
                status: Sring  ALERTA, ERROR, INFO
                info{}: diccionario o lista compatible json
                modelo_id(opcional): id unica del objeto del Log
            Returns:
                Log
        """
        logsupermercado = LogSupermercado()
        logsupermercado.user_id = user_id
        logsupermercado.grupo = grupo
        logsupermercado.tipo = tipo
        logsupermercado.status = status
        logsupermercado.info = info
        logsupermercado.modelo_id = modelo_id
        logsupermercado.save()
        return logsupermercado


    @staticmethod
    def obtenerLogSupermercado(logsupermercado_id):
        """
            Función que obtiene un logsupermercado especifico
            Param:
                logsupermercado_id: id del logsupermercado a buscar
            Return:
                LogSupermercado
                None en caso de no existir el Log
        """
        try:
            return LogSupermercado.objects.get(id=logsupermercado_id)
        except Exception,e:
            return None

    @staticmethod
    def obtenerLogsSupermercado(**kwargs):
        """
            Función para obtener un conjunto de LogsSupermercado según los criterios especificados
            Params:
                user_id
                users_id
                grupo
                grupos
                tipo
                tipos
                status
                user_id
                modelo_id
                modelo_ids
                limit
            QuerySet<Log>
        """
        logssupermercado = LogSupermercado.objects.all()
        if 'user_id' in kwargs:
            logssupermercado = logssupermercado.filter(user_id=kwargs['user_id'])
        if 'users_id' in kwargs:
            logssupermercado = logssupermercado.filter(user_id__in=kwargs['users_id'])

        if 'grupo' in kwargs:
            logssupermercado = logssupermercado.filter(grupo=kwargs['grupo'])
        if 'grupos' in kwargs:
            logssupermercado = logssupermercado.filter(grupo__in=kwargs['grupos'])

        if 'tipo' in kwargs:
            logssupermercado = logssupermercado.filter(tipo=kwargs['tipo'])
        if 'tipos' in kwargs:
            logssupermercado = logssupermercado.filter(tipo__in=kwargs['tipos'])

        if 'status' in kwargs:
            logssupermercado = logssupermercado.filter(status=kwargs['status'])

        if 'user_id' in kwargs:
            logssupermercado = logssupermercado.filter(user_id__in=kwargs['user_id'])
        
        if 'modelo_id' in kwargs:
            logssupermercado = logssupermercado.filter(modelo_id=kwargs['modelo_id'])
        if 'modelo_ids' in kwargs:
            logssupermercado = logssupermercado.filter(modelo_id__in=kwargs['modelo_ids'])

        if 'limit' in kwargs:
            logssupermercado = logssupermercado[:kwargs['limit']]
        return logssupermercado


class ManagerConfiguracionSupermercado():

    NUMERO = 'ERROR'
    TEXTO = 'TEXTO'
    JSON = 'JSON'
    FECHA = 'FECHA'


    @staticmethod
    def obtenerConfiguracionSupermercado(configuracionsupermercado_id):
        """
            Función que obtiene un configuracionsupermercado especifico
            Param:
                configuracionsupermercado_id: id del configuracionsupermercado a buscar
            Return:
                ConfiguracionSupermercado
                None en caso de no existir el ConfiguracionSupermercad
        """
        try:
            return ConfiguracionSupermercado.objects.get(id=configuracionsupermercado_id)
        except Exception,e:
            return None


    @staticmethod
    def obtenerConfiguracionesSupermercado(**kwargs):
        """
            Función para obtener un conjunto de LogsSupermercado según los criterios especificados
            Params:
                nombre
                nombres
                tipo
                tipos
            QuerySet<Log>
        """
        configuracionessupermercado = ConfiguracionSupermercado.objects.all()
        if 'nombre' in kwargs:
            configuracionessupermercado = configuracionessupermercado.filter(nombre=kwargs['nombre'])
        if 'nombres' in kwargs:
            configuracionessupermercado = configuracionessupermercado.filter(nombre__in=kwargs['nombres'])

        if 'tipo' in kwargs:
            configuracionessupermercado = configuracionessupermercado.filter(tipo=kwargs['tipo'])
        if 'tipos' in kwargs:
            configuracionessupermercado = configuracionessupermercado.filter(tipo__in=kwargs['tipos'])

        if 'limit' in kwargs:
            configuracionessupermercado = configuracionessupermercado[:kwargs['limit']]
        return configuracionessupermercado



    @staticmethod
    def crearConfiguracionSupermercado(nombre, valor, tipo):
        """
            Función para crear un ConfiguracionSupermercado
            Params:
                nombre: nombre de la variable 
                valor: valor de la variable puede ser Numero, texto, json, fecha
                tipo: Tipo de la variable a guardar NUMERO, TEXTO, JSON, FECHA
            Returns:
                ConfiguracionSupermercado
        """
        configuracionsupermercado = None

        configuracionessupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre=nombre)
        if configuracionessupermercado.count() > 0 :
            configuracionsupermercado = configuracionessupermercado[0]
        else:
            configuracionsupermercado = ConfiguracionSupermercado()
            configuracionsupermercado.nombre = nombre
        configuracionsupermercado.tipo = tipo
        configuracionsupermercado.valor = valor
        configuracionsupermercado.save()
        return configuracionsupermercado


    @staticmethod
    def actualizarConfiguracionSupermercado(configuracionsupermercado, valor, tipo=None ):
        """
            Función para actualizar ConfiguracionSupermercado
            Params:
                <Integer>(id configuracion)
                <String>(nombre configuracion)
                <ConfiguracionSupermercado>(Objeto)
                     configuracionsupermercado_id: configuracion supermercado
                valor: debe ser del mismo tipo de la configuracion
                tipo:(opcional)
            Returns:
                ConfiguracionSupermercado
        """
        aux_configuracionsupermercado = None
        if type(configuracionsupermercado) == type(1):
            aux_configuracionsupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionSupermercado(configuracionsupermercado)
        elif type(configuracionsupermercado) == type('string'):
            configuracionessupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre=configuracionsupermercado)
            if configuracionessupermercado.count() > 0 :
                aux_configuracionsupermercado = configuracionessupermercado[0]
        elif type(configuracionsupermercado) == type(ConfiguracionSupermercado()):
            aux_configuracionsupermercado = configuracionsupermercado
        configuracionsupermercado = aux_configuracionsupermercado
        if configuracionsupermercado is None:
            return None
        if tipo is not None:
            configuracionsupermercado.tipo = tipo
        configuracionsupermercado.valor = valor
        configuracionsupermercado.save()
        return configuracionsupermercado


    @staticmethod
    def eliminarConfiguracionSupermercado(configuracionsupermercado_id):
        """
            Función para eliminar ConfiguracionSupermercado
            Params:
                <Integer>(id configuracion)
                <String>(nombre configuracion)
                <ConfiguracionSupermercado>(Objeto)
                     configuracionsupermercado_id: configuracion supermercado
            Returns:
                ConfiguracionSupermercado
        """
        aux_configuracionsupermercado = None
        if type(configuracionsupermercado) == type(1):
            aux_configuracionsupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionSupermercado(configuracionsupermercado)
        elif type(configuracionsupermercado) == type('string'):
            configuracionessupermercado = ManagerConfiguracionSupermercado.obtenerConfiguracionesSupermercado(nombre=configuracionsupermercado)
            if configuracionessupermercado.conut() > 0 :
                aux_configuracionsupermercado = configuracionessupermercado[0]
        elif type(configuracionsupermercado) == type(ConfiguracionSupermercado()):
            aux_configuracionsupermercado = configuracionsupermercado
        configuracionsupermercado = aux_configuracionsupermercado
        if configuracionsupermercado is None:
            return None
        configuracionsupermercado.delete()
        return None


