# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 19:52'

from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('active/<slug:active_code>/', views.ActiveCode.as_view(), name='user_active'),
    path('forget_password/', views.ForgetPassword.as_view(), name='forget_password'),
    path('forget/<slug:user_name>/<slug:forget_password_code>/', views.ForgetPassWordCode.as_view(), name='reset_password_verify'),
    path('reset_password/', views.ResetPassword.as_view(), name='reset_password'),

]