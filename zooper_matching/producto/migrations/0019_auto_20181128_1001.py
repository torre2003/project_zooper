# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-28 10:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0018_auto_20181126_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productojumbo',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 10, 1, 18, 629931)),
        ),
        migrations.AlterField(
            model_name='productolider',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 10, 1, 18, 629064)),
        ),
        migrations.AlterField(
            model_name='productotelemercado',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 10, 1, 18, 630737)),
        ),
        migrations.AlterField(
            model_name='productotottus',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 10, 1, 18, 631574)),
        ),
    ]
