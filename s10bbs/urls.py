"""s10bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from bbs import views
from django.views.static import serve
from django.conf import settings
from bbs import urls as blog_urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include(blog_urls)),


    url(r'^login/', views.login),
    url(r'^yzm/', views.ver),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^up/', views.up),
    url(r'^reg/', views.regis),
    url(r'^media/(?P<path>.*)$',serve,{"document_root": settings.MEDIA_ROOT}),
    url(r'^upload/', views.upload),

]
