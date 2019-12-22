# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-28 10:18
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticuloLider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=40, null=True)),
                ('nombre', models.CharField(max_length=300, null=True)),
                ('marca', models.CharField(max_length=100, null=True)),
                ('url_imagen', models.CharField(max_length=300, null=True)),
                ('url_producto', models.CharField(max_length=300, null=True)),
                ('caracteristica', models.CharField(max_length=50, null=True)),
                ('precio_alto', models.IntegerField(default=0)),
                ('precio_bajo', models.IntegerField(default=0)),
                ('precio_unidad_medida', models.CharField(max_length=50, null=True)),
                ('etiquetas_precio', django.contrib.postgres.fields.jsonb.JSONField(default={}, null=True)),
                ('etiquetas_oferta', django.contrib.postgres.fields.jsonb.JSONField(default={}, null=True)),
                ('estado', models.CharField(choices=[('OK', 'OK'), ('ERROR', 'ERROR'), ('DESHABILITADO', 'DESHABILITADO')], max_length=30, null=True)),
                ('estado_mensaje', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InfoActualizacionArticuloLider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_actualizacion', models.CharField(max_length=300, null=True)),
                ('estado', models.CharField(choices=[('NO_ACTUALIZADO', 'NO_ACTUALIZADO'), ('ACTUALIZADO', 'ACTUALIZADO'), ('PENDIENTE_ACTUALIZACION', 'PENDIENTE_ACTUALIZACION'), ('ERROR', 'ERROR')], max_length=30, null=True)),
                ('estado_mensaje', models.CharField(max_length=100, null=True)),
                ('ultima_actualizacion', models.DateTimeField(auto_now_add=True)),
                ('articulolider', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lider.ArticuloLider')),
            ],
        ),
        migrations.CreateModel(
            name='InfoBusquedaArticuloLider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_busqueda', models.CharField(max_length=300, null=True)),
                ('estado', models.CharField(choices=[('ENCONTRADO', 'ENCONTRADO'), ('EN_PROCESO', 'EN_PROCESO'), ('NO_ENCONTRADO', 'NO_ENCONTRADO')], max_length=30, null=True)),
                ('intentos', models.IntegerField(default=0)),
                ('ultima_actualizacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]