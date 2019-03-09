#coding:utf-8
'''
from django import VERSION
if VERSION[0:2]>(1,3):
    from django.conf.urls import url
else:
    from django.conf.urls.defaults import patterns, url


'''
from django.urls import path
from django.conf.urls import url
from .views import get_ueditor_controller


urlpatterns = [
    path('controller/', get_ueditor_controller),
]
