# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import JSONField, ArrayField

from django.contrib.auth.models import User


class ConfiguracionSupermercado(models.Model):
    NUMERO = 'NUMERO'
    DECIMAL = 'DECIMAL'
    TEXTO = 'TEXTO'
    JSON = 'JSON'
    FECHA = 'FECHA'

    TIPO = (
        (NUMERO, 'NUMERO'),
        (DECIMAL, 'DECIMAL'),
        (TEXTO, 'TEXTO'),
        (JSON, 'JSON'),
        (FECHA, 'FECHA'),
    )
    nombre = models.CharField(max_length=200)
    _valor = models.TextField()
    tipo = models.CharField(max_length=30,choices=TIPO, null=True)

    def get_valor(self):
        if self.tipo == 'NUMERO':
            return int(self._valor)
        elif self.tipo == 'DECIMAL':
            return float(self._valor)
        elif self.tipo == 'TEXTO':
            return self._valor
        elif self.tipo == 'JSON':
            return json.loads(self._valor)
        elif self.tipo == 'FECHA':
            #_valor.strptime(d,"%Y-%m-%d %H:%M:%S")
            return datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
        else:
            raise Exception('No existe el tipo especificado')

    def set_valor(self, value):
        if self.tipo == 'NUMERO':
            self._valor = unicode (value)
        elif self.tipo == 'DECIMAL':
            self._valor = unicode (value)
        elif self.tipo == 'TEXTO':
            self._valor = value
        elif self.tipo == 'JSON':
            self._valor = json.dumps(value, ensure_ascii=False)
        elif self.tipo == 'FECHA':
            self._valor = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            raise Exception('No existe el tipo especificado')

    valor = property(get_valor, set_valor)



class LogSupermercado(models.Model):
    ALERTA = 'ALERTA'
    ERROR = 'ERROR'
    INFO = 'INFO'

    STATUS = (
        (ALERTA, 'ALERTA'),
        (ERROR, 'ERROR'),
        (INFO, 'INFO'),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.DO_NOTHING, null=True)
    grupo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS, null=True)
    modelo_id = models.IntegerField(default=0, null=True)
    info = JSONField()

