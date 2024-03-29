# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-18 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumbo', '0004_auto_20181016_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoBusquedaArticuloJumbo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador_busqueda', models.CharField(max_length=20, null=True)),
                ('estado', models.CharField(choices=[('ENCONTRADO', 'ENCONTRADO'), ('EN_PROCESO', 'EN_PROCESO'), ('NO_ENCONTRADO', 'NO_ENCONTRADO')], max_length=30, null=True)),
                ('intentos', models.IntegerField(default=0)),
                ('ultima_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
