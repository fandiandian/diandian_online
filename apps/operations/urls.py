# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/25 18:14'

from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    # 用户个人中心
    path('user_center_information/', views.UserCenterInformation.as_view(), name='user_center_information'),

    # 用户学习的课程
    path('user_center_my_courses/', views.UserStudyCourse.as_view(), name='user_center_my_courses'),

    # 用户消息
    path('user_center_messages/', views.UserMessageView.as_view(), name='user_center_messages'),

    # 用户收藏的教师
    path('user_center_fav_teachers/', views.UserCollectedTeacher.as_view(), name='user_center_fav_teachers'),
    # 用户收藏的教师
    path('user_center_fav_courses/', views.UserCollectedCourse.as_view(), name='user_center_fav_courses'),
    # 用户收藏的教师
    path('user_center_fav_organizations/', views.UserCollectedOrganization.as_view(), name='user_center_fav_organizations'),

    # 修改用户头像
    path('reset_head_portrait/', views.ResetUserHeaderPortraitView.as_view(), name='reset_head_portrait'),
    # 修改用户密码
    path('reset_user_password/', views.ResetUserPasswordView.as_view(), name='reset_user_password'),
    # 修改用户信息
    path('reset_user_information/', views.ResetUserInformationView.as_view(), name='reset_user_information'),
    # 修改邮箱是发送的验证码
    path('send_email_verify_record/', views.SendEmailView.as_view(), name='send_email_verify_record'),
    # 修改邮箱
    path('reset_user_email/', views.ResetUserEmailView.as_view(), name='reset_user_email'),

    # 读取用户消息
    path('read_message/', views.ReadMessageView.as_view(), name='read_message'),


]