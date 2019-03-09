# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/3/6 22:24'

import re

from django import forms
from users.models import UserProfiles


class ResetUserHeaderPortraitForm(forms.ModelForm):

    class Meta:
        model = UserProfiles
        fields = ['head_portrait']


class ResetUserPasswordForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=16)
    password2 = forms.CharField(required=True, min_length=6, max_length=16)


class SendEmailForm(forms.Form):
    email = forms.EmailField(required=True)


class ResetUserInformationForm(forms.ModelForm):

    class Meta:
        model = UserProfiles
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        regex = r'^1[3|4|5|7|8]\d{9}$'
        pattern = re.compile(regex)
        if pattern.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'无效的手机号码', code='mobile_invalid')