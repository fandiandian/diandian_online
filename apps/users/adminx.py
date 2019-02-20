# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 1:06'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, ViewPage


class BaseSetting:
    # 更改后台的主题样式
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    # 更改后台的标题和页脚显示
    site_title = u"点点后台管理系统"
    site_footer = u"点点在线网"
    # 应用模型在后台页面导航栏显示为下拉样式
    menu_style = "accordion"


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
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)