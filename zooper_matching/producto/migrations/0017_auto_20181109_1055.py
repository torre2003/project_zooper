# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-09 10:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0016_auto_20181107_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productojumbo',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 10, 55, 18, 634541)),
        ),
        migrations.AlterField(
            model_name='productolider',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 10, 55, 18, 633599)),
        ),
        migrations.AlterField(
            model_name='productotelemercado',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 10, 55, 18, 635355)),
        ),
        migrations.AlterField(
            model_name='productotottus',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 10, 55, 18, 636298)),
        ),
    ]
