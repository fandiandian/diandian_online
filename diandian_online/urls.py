# _*_ coding: utf-8 _*_

"""diandian_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import xadmin
from django.views.generic import TemplateView

# 静态文件请求的处理
from django.views.static import serve
from diandian_online import settings
from apps.users import views


urlpatterns = [

    # 首页
    path('', views.Index.as_view(), name='index'),
    # xadmin 的后台
    path('xadmin/', xadmin.site.urls),

    # 用户相关的页面
    path('users/', include('users.urls')),
    # 用户操作相关的页面
    path('operations/', include('operations.urls')),
    # 课程页面
    path('courses/', include('courses.urls')),
    # 机构页面
    path('organizations/', include('organizations.urls')),

    # 配置验证码
    path('captcha/', include('captcha.urls')),
    # 配置图片请求
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),

    # xadmin 第三方的富文本插件
    path('ueditor/',include('DUEditor.urls' )),

    # 配置未上线时的错误页面调试的静态文件路径
    # path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
]


# 404 错误页面 （一般是错误的 url 导致的)
handler404 = 'users.views.handler_404_error'
handler500 = 'users.views.handler_500_error'
handler403 = 'users.views.handler_403_error'
