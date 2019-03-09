# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/28 23:11'

import re

from django import forms

from operations.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

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