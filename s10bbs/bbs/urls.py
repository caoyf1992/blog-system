# !/usr/bin/python
# -*- coding: UTF-8 -*-
# Author：Cao yf

from django.conf.urls import url
from bbs import views

urlpatterns = [


    url(r"dele/", views.dele),
    url(r"edit/", views.edit),
    url(r"add_blog/", views.add_blog),

    url(r"up_down/",views.up_down),
    url(r"pinglun/",views.pinglun),

    url(r'^(\w+)/article/(\d+)/$', views.article),

    url(r'^(\w+)/(article|tag|archive)/(.+)/$', views.home),


    url(r'^(\w+)/',  views.home),

    ]