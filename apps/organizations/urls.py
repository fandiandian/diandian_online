# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/25 21:47'

from django.urls import path

from . import views

app_name = 'organizations'

urlpatterns = [
    # 课程机构列表
    path('organizations_list/', views.OrganizationsList.as_view(), name='organizations_list'),
    # 课程咨询
    path('add_ask/', views.AddUserAsk.as_view(), name='add_ask'),
    # 机构详情
    path('organization_detail_homepage/<int:org_id>/', views.OrganizationHomePage.as_view(), name='organization_detail_homepage'),
    path('organization_detail_courses/<int:org_id>/', views.OrganizationCoursePage.as_view(), name='organization_detail_courses'),
    path('organization_detail_teachers/<int:org_id>/', views.OrganizationTeacherPage.as_view(), name='organization_detail_teachers'),
    path('organization_detail_description/<int:org_id>/', views.OrganizationDescripthionPage.as_view(), name='organization_detail_description'),
    # 收藏功能
    path('add_collection', views.AddCollection.as_view(), name='add_collection'),


    path('teacher_detail/<int:teacher_id>', views.TeacherInformation.as_view(), name='teacher_detail'),
    path('teachers_list/', views.TeacherList.as_view(), name='teachers_list'),
]