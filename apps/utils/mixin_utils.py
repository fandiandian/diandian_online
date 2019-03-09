# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/3/6 20:23'


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin:

    @method_decorator(login_required(login_url='/users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

