# _*_ coding: utf-8 _*_

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # 为模型定义别名
    verbose_name = u'用户管理'
