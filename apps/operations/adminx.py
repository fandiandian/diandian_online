# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 2:14'

import xadmin

from .models import UserProfiles, UserMessage, UserAsk, UserCollection, UserCourse, CourseComment


class CourseCommentAdmin:
    list_display = ['user', 'course', 'teacher', 'course_mark', 'teacher_mark', 'comment', 'add_time']
    list_filter = ['user', 'course', 'teacher', 'course_mark', 'teacher_mark', 'comment']
    search_fields = ['user', 'course', 'teacher', 'course_mark', 'teacher_mark', 'comment', 'add_time']


class UserMessageAdmin:
    list_display = ['user', 'message', 'has_read', 'send_time']
    list_filter = ['user', 'message', 'has_read']
    search_fields = ['user', 'message', 'has_read', 'send_time']


class UserAskAdmin:
    list_display = ['name', 'mobile', 'course_name', 'question', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'question']
    search_fields = ['name', 'mobile', 'course_name', 'question', 'add_time']


class UserCollectionAdmin:
    list_display = ['user', 'collection_id', 'collection_type', 'add_time']
    list_filter = ['user', 'collection_id', 'collection_type']
    search_fields = ['user', 'collection_id', 'collection_type', 'add_time']


class UserCourseAdmin:
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course']
    search_fields = ['user', 'course', 'add_time']


xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCollection, UserCollectionAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)