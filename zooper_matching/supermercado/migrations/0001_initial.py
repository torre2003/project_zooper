# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('_valor', models.TextField()),
                ('tipo', models.CharField(choices=[('ERROR', 'NUMERO'), ('TEXTO', 'TEXTO'), ('JSON', 'JSON'), ('FECHA', 'FECHA')], max_length=30, null=True)),
            ],
        ),
    ]
