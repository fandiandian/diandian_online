# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/21 19:33'

from django import forms
from captcha.fields import CaptchaField


# 注册时后台表单验证
class RegisterForm(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=16)
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 登录时后台表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


# 找回密码时的表单验证
class ForgetPasswordForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=16)
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetPasswordForm(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=16)
    password2 = forms.CharField(required=True, min_length=6, max_length=16)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})