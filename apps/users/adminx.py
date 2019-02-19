# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 1:06'

import xadmin

from .models import EmailVerifyRecord, ViewPage


# 此处不要继承任何类。默认继承 python 的 object
class EmailVerifyRecordAdmin:
    # 用于展示邮件验证码这张表的信息
    # 按 email, code, send_type, send_time 的列方式显式
    list_display = ['email', 'code', 'send_type', 'send_time']
    # 通过设定 search_fields 字段来实现对数据表的「查」操作
    search_fields = ['email', 'code', 'send_type']
    # list_filter 实现筛选功能
    list_filter = ['email', 'code', 'send_type', 'send_time']


class ViewPageAdmin:
    list_display = ['index', 'title', 'image', 'url', 'add_time']
    search_fields = ['index', 'title', 'image', 'url']
    list_filter = ['index', 'title', 'image', 'url', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(ViewPage, ViewPageAdmin)