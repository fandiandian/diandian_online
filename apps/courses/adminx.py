# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 2:14'

import xadmin

from .models import Course, CourseResource, Chapter, Section


class CourseAdmin:
    list_display = ['course_name', 'description', 'detail', 'degree',
                    'learn_times', 'student_number', 'collect_number',
                    'course_mark', 'course_image', 'click_number', 'add_time']
    list_filter = ['course_name', 'description', 'detail', 'degree',
                    'learn_times', 'student_number', 'collect_number',
                    'course_mark', 'course_image', 'click_number']
    search_fields = ['course_name', 'description', 'detail', 'degree',
                    'learn_times', 'student_number', 'collect_number',
                    'course_mark', 'course_image', 'click_number', 'add_time']


class CourseResourceAdmin:
    list_display = ['course', 'resource_name', 'download', 'add_time']
    list_filter = ['course', 'resource_name', 'download']
    search_fields = ['course', 'resource_name', 'download', 'add_time']


class ChapterAdmin:
    list_display = ['course', 'chapter_name', 'add_time']
    list_filter = ['course__course_name', 'chapter_name']
    search_fields = ['course', 'chapter_name', 'add_time']


class SectionAdmin:
    list_display = ['chapter', 'section_name', 'add_time']
    list_filter = ['chapter__chapter_name', 'section_name']
    search_fields = ['chapter', 'section_name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Section, SectionAdmin)

