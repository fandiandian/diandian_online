# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/22 21:03'

import random

from django.core.mail import send_mail
from diandian_online.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


# 定义邮件验证码：并保存到数据库中，以便比对验证
def send_email_verify_record(email, send_type='register', username=''):
    email_verify_record = EmailVerifyRecord()
    code = random_str()
    email_verify_record.code = code
    email_verify_record.email = email
    email_verify_record.send_type = send_type
    email_verify_record.save()

    # 邮件的标题和邮件内容
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '点点在线网注册激活链接'
        email_body = '请点击的链接激活你的账号：http://127.0.0.1:8000/users/active/{0}'.format(code)
    elif send_type == 'forget':
        email_title = '点点在线网找回密码链接'
        email_body = '请点击的链接重置你的密码：http://127.0.0.1:8000/users/forget/{0}/{1}'.format(username, code)
    elif send_type == 'reset_email':
        email_title = '点点在线网重置邮箱验证码'
        email_body = '请将邮件的的验证码填写至修改邮箱的页面中：{0}'.format(code)

    # 使用 try 来避免网络波动，或者邮件后台配制错误引发的错误，如果没有问题，返回一个 True
    try:
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    except Exception as e:
        return False
    else:
        if send_status:
            return True
        else:
            return False



def random_str(length=8):
    str = ''
    temp_str = 'ABCDEFGHIJKLMNOPQRETUVWXYZabcedfghijklmnopqrstuvwxyz0123456789'
    for i in range(length):
        str += temp_str[random.randint(0, len(temp_str) - 1)]
    return str

