# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-12 13:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0008_auto_20181011_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productojumbo',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 12, 10, 6, 15, 947615)),
        ),
        migrations.AlterField(
            model_name='productolider',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 12, 10, 6, 15, 946225)),
        ),
        migrations.AlterField(
            model_name='productotelemercado',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 12, 10, 6, 15, 948811)),
        ),
        migrations.AlterField(
            model_name='productotottus',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 12, 10, 6, 15, 950088)),
        ),
    ]
