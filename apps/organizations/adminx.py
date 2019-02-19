# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 2:14'

import  xadmin

from .models import CourseOrganization, CityDict, Teacher


class CityDictAdmin:
    list_display = ['city_name', 'description', 'add_time']
    list_filter = ['city_name', 'description']
    search_fields = ['city_name', 'description', 'add_time']


class CourseOrganizationAdmin:
    list_display = ['organization_name', 'description', 'collect_number', 'click_number',
                    'organization_image', 'address', 'city', 'add_time']
    list_filter = ['organization_name', 'description', 'collect_number', 'click_number',
                    'organization_image', 'address', 'city']
    search_fields = ['organization_name', 'description', 'collect_number', 'click_number',
                    'organization_image', 'address', 'city', 'add_time']


class TeacherAdmin:
    list_display = ['organization', 'teacher_name', 'description', 'teacher_mark',
                    'inauguration_company', 'company_position', 'work_year',
                    'collect_number', 'click_number', 'teacher_image', 'add_time']
    list_filter = ['organization', 'teacher_name', 'description', 'teacher_mark',
                    'inauguration_company', 'company_position', 'work_year',
                    'collect_number', 'click_number', 'teacher_image']
    search_fields = ['organization', 'teacher_name', 'description', 'teacher_mark',
                    'inauguration_company', 'company_position', 'work_year',
                    'collect_number', 'click_number', 'teacher_image', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrganization, CourseOrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)