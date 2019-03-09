# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 2:14'

import  xadmin

from .models import CourseOrganization, CityDict, Teacher


# 定义机构关联的教师
class TeacherInline:
    model = Teacher
    extra = 0


class CityDictAdmin:
    list_display = ['city_name', 'description', 'add_time']
    list_filter = ['city_name', 'description']
    search_fields = ['city_name', 'description', 'add_time']


class CourseOrganizationAdmin:
    list_display = ['organization_name', 'collect_number', 'click_number', 'students',
                    'address', 'city', 'add_time', 'tag']
    list_filter = ['organization_name', 'description', 'collect_number', 'click_number',
                    'address', 'city']
    search_fields = ['organization_name', 'collect_number', 'click_number',
                     'address', 'city', 'add_time']
    inlines = [TeacherInline]
    # 定义列表显示的排序，以点击量的倒序排列
    ordering = ['-click_number']
    # 定义字段为可读字段
    readonly_fields = ['collect_number', 'click_number', 'organization_mark', 'students', 'course_number']
    # 通过这个关键字的声明，某些字段可以列表的时候就可以完成修改
    list_editable = [
        'organization_name', 'address', 'description', 'city', 'tag'
    ]
    # 定义机构描述的展示样式
    style_fields = {'description': 'ueditor'}
    # excel 文件的导入功能
    import_excel = True

    # 重载 post 方法，实现 excel 数据的上传
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            # 这里的代码可以自己写，比如说需要保存某些数据
            pass
        return super().post(request, args, kwargs)


class TeacherAdmin:
    list_display = ['organization', 'teacher_name', 'teacher_mark',
                    'inauguration_company', 'company_position', 'get_course_number_teacher',
                    'collect_number', 'click_number', 'add_time']
    list_filter = ['organization', 'teacher_name', 'description', 'teacher_mark',
                    'inauguration_company', 'company_position', 'work_year',
                    'collect_number', 'click_number']
    search_fields = ['organization', 'teacher_name', 'teacher_mark',
                    'inauguration_company', 'company_position', 'work_year',
                    'collect_number', 'click_number', 'add_time']
    ordering = ['-click_number']
    readonly_fields = ['collect_number', 'click_number', 'teacher_mark']
    list_editable = [
        'teacher_name', 'description', 'inauguration_company', 'company_position', 'work_year',
    ]
    # 定义教师描述的展示样式
    style_fields = {'description': 'ueditor'}
    # excel 文件的导入功能
    import_excel = True

    # 重载 post 方法，实现 excel 数据的上传
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super().post(request, args, kwargs)




xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrganization, CourseOrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)