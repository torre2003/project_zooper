# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-16 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumbo', '0002_auto_20181011_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulojumbo',
            name='validez_precio',
            field=models.DateTimeField(null=True),
        ),
    ]