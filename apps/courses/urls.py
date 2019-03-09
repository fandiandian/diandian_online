# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/25 21:47'

from django.urls import path


from . import views

app_name = 'courses'

urlpatterns = [
    path('specialized_courses_list/', views.SpecializedCoursesList.as_view(), name='specialized_courses_list'),
    path('open_courses_list/', views.OpenCoursesList.as_view(), name='open_courses_list'),
    path('course_detail/<int:course_id>/', views.CourseDetail.as_view(), name='course_detail'),

    # 课程学习
    path('course_study/<int:course_id>/', views.CourseStudy.as_view(), name='course_study'),
    # 课程评论
    path('course_comment/<int:course_id>/', views.CourseCommentView.as_view(), name='course_comment'),
    # 添加课程评论
    path('add_course_comment/', views.AddCourseCommentView.as_view(), name='add_course_comment'),
    # 添加课程到用户的学习表
    path('add_course_study',views.AddCourseStudy.as_view(), name='add_course_study'),
    # 课程的章节学习页面
    path('course_study_detail/<int:course_id>/<int:section_id>/', views.CourseStudyDetail.as_view(), name='course_study_detail'),
]