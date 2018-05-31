# !/usr/bin/python
# -*- coding: UTF-8 -*-
# Author：Cao yf
from django import template
from bbs import models
from django.db.models import Count
register = template.Library()

@register.inclusion_tag('youce.html')
def get_list(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    ret = models.Category.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')

    ret1 = models.Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('title','c')

    ret2 = models.Article.objects.filter(user=user).extra(
        select={'archive_time':"date_format(create_time,'%%Y-%%m')"}
    ).values('archive_time').annotate(archive=Count('nid')).values('archive_time','archive')

    return  {'ret':ret,'ret1':ret1,'ret2':ret2,'username':username}