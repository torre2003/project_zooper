# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from apps import AccountsConfig


app_name = AccountsConfig.name

urlpatterns = [
    url(r'^$', views.view_index, name='index'),
    #url(r'^sin-permisos/$', views.sin_permisos, name='sin-permisos'),
]