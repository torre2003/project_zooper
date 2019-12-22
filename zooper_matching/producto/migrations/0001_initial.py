# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-25 12:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoJumbo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, null=True)),
                ('image_urls', models.CharField(max_length=200, null=True)),
                ('marca', models.CharField(max_length=50, null=True)),
                ('precio', models.CharField(max_length=20, null=True)),
                ('titulo', models.CharField(max_length=1000, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoLider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, null=True)),
                ('caracteristica', models.CharField(max_length=50, null=True)),
                ('precio', models.CharField(max_length=15, null=True)),
                ('precio_unidad_medida', models.CharField(max_length=25, null=True)),
                ('sub_titulo', models.CharField(max_length=100, null=True)),
                ('titulo', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoTelemercado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, null=True)),
                ('detalle', models.CharField(max_length=1000, null=True)),
                ('precio', models.CharField(max_length=20, null=True)),
                ('titulo', models.CharField(max_length=100, null=True)),
                ('url_imagen', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoTottus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, null=True)),
                ('link', models.CharField(max_length=200, null=True)),
                ('marca', models.CharField(max_length=40, null=True)),
                ('medida', models.CharField(max_length=50, null=True)),
                ('nombre', models.CharField(max_length=100, null=True)),
                ('precio', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoZooper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medida', models.CharField(max_length=50, null=True)),
                ('precio', models.CharField(max_length=15, null=True)),
                ('precio_unidad_medida', models.CharField(max_length=25, null=True)),
                ('nombre_producto', models.CharField(max_length=100, null=True)),
                ('marca', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='productotottus',
            name='productozooper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='producto.ProductoZooper'),
        ),
        migrations.AddField(
            model_name='productotelemercado',
            name='productozooper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='producto.ProductoZooper'),
        ),
        migrations.AddField(
            model_name='productolider',
            name='productozooper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='producto.ProductoZooper'),
        ),
        migrations.AddField(
            model_name='productojumbo',
            name='productozooper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='producto.ProductoZooper'),
        ),
    ]
