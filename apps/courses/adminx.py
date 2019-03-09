# _*_ coding: utf-8 _*_
__author__ = 'nick'
__date__ = '2019/2/20 2:14'

import xadmin

from .models import Course, CourseResource, Chapter, Section, CourseCategory, CourseType, BannerCourse
from .models import CourseAnnouncement, CourseNotice, Tags
from organizations.models import CourseOrganization, Teacher


# 定义课程的关联章节
class ChapterInline:
    model = Chapter
    extra = 0


# 定义课程关联的课程资源
class ResourceInline:
    model = CourseResource
    extra = 0


# 定义章节关联的小节信息
class SectionInline:
    model = Section
    extra = 0


# 定义课程大类关联的小类
class CourseTypeInline:
    model = CourseType
    extra = 0


class CourseAdmin:
    list_display = ['course_name', 'degree', 'course_teacher','course_tag',
                    'student_number', 'collect_number', 'is_banner',
                    'course_mark', 'click_number', 'add_time']
    list_filter = ['course_name', 'degree', 'course_teacher', 'is_banner',
                    'learn_times', 'student_number', 'collect_number',
                    'course_mark', 'click_number']
    search_fields = ['course_name', 'degree', 'course_teacher','course_tag',
                    'student_number', 'collect_number', 'is_banner',
                    'course_mark', 'click_number', 'add_time']
    inlines = [ChapterInline, ResourceInline]
    ordering = ['-click_number']
    readonly_fields = ['student_number', 'collect_number', 'course_mark', 'click_number']
    # 通过这个关键字的声明，某些字段可以列表的时候就可以完成修改
    list_editable = [
        'course_tag', 'degree', 'description', 'course_name', 'is_banner', 'open_type'
    ]
    # 定义课程描述的样式
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    # 这里是调用的 super 函数，这是一种特殊的写法
    # 在 python2 和 python3 中有区别
    # python2 --> super(CourseAdmin, self).queryset()
    # 在这里 xadmin 在后台进行注册的时候，将当前的类 CourseAdmin 和 Course 这个列进行了关联
    # 实际上是通过继承，将函数 queryset 添加到 Course 中，在 Course 的实例上调用的 queryset 函数
    # 调用的结果就是 filter 是筛选出符合条件的课程
    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner='False')
        return qs

    # 当添加新的课程的时候，重新统计机构的课程数量，并进行更新
    def save_models(self):
        # 这里是新建课程的时候，用 new_obj 来指代这个新建的课程实例
        obj = self.new_obj
        obj.save()
        if obj.course_teacher:
            org = obj.course_teacher.organization
            teachers = [teacher.id for teacher in Teacher.objects.filter(organization=org)]
            org.course_number = Course.objects.filter(course_teacher__in=teachers).count()
            org.save()

    # 重载 post 方法，实现 excel 数据的上传
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super().post(request, args, kwargs)



class BannerCourseAdmin:
    list_display = ['course_name', 'degree', 'course_teacher','course_tag',
                    'student_number', 'collect_number', 'is_banner',
                    'course_mark', 'click_number', 'add_time']
    list_filter = ['course_name', 'degree', 'course_teacher', 'is_banner',
                    'learn_times', 'student_number', 'collect_number',
                    'course_mark', 'click_number']
    search_fields = ['course_name', 'degree', 'course_teacher','course_tag',
                    'student_number', 'collect_number', 'is_banner',
                    'course_mark', 'click_number', 'add_time']
    inlines = [ChapterInline, ResourceInline]
    ordering = ['-click_number']
    readonly_field = ['student_number', 'collect_number', 'course_mark', 'click_number']
    list_editable = [
        'course_tag', 'degree', 'description', 'course_name', 'is_banner', 'open_type'
    ]
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner='True')
        return qs

    # 当添加新的课程的时候，重新统计机构的课程数量，并进行更新
    def save_models(self):
        # 这里是新建课程的时候，用 new_obj 来指代这个新建的课程实例
        obj = self.new_obj
        obj.save()
        if obj.course_teacher:
            org = obj.course_teacher.organization
            teachers = [teacher.id for teacher in Teacher.objects.filter(organization=org)]
            org.course_number = Course.objects.filter(course_teacher__in=teachers).count()
            org.save()

    # 重载 post 方法，实现 excel 数据的上传
    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super().post(request, args, kwargs)



class CourseResourceAdmin:
    list_display = ['course', 'resource_name', 'download', 'add_time']
    list_filter = ['course', 'resource_name', 'download']
    search_fields = ['course', 'resource_name', 'download', 'add_time']
    list_editable = ['resource_name']


class ChapterAdmin:
    list_display = ['course', 'chapter_name', 'add_time']
    list_filter = ['course__course_name', 'chapter_name']
    search_fields = ['course', 'chapter_name', 'add_time']
    inlines = [SectionInline]
    list_editable = ['chapter_name']



class SectionAdmin:
    list_display = ['chapter', 'section_name', 'add_time']
    list_filter = ['chapter__chapter_name', 'section_name']
    search_fields = ['chapter', 'section_name', 'add_time']
    list_editable = ['section_name']


# 课程大类
class CourseCategoryAdmin:
    list_display = ['course_category', 'add_time']
    search_fields = ['course_category', 'add_time']
    inlines = [CourseTypeInline]
    list_editable = ['course_category']


# 课程小类
class CourseTypeAdmin:
    list_display = ['course_category', 'course_type', 'add_time']
    list_filter = ['course_category__course_category']
    search_fields = ['course_category', 'course_type', 'add_time']
    list_editable = ['course_type']

class CourseAnnouncementAdmin:
    list_display = ['course', 'course_announcement', 'add_time']
    list_filter = ['course']
    search_fields = ['course_category', 'course_type', 'add_time']
    list_editable = ['course_announcement']


class CourseNoticeAdmin:
    list_display = ['course', 'course_notice', 'course_goal', 'add_time']
    list_filter = ['course']
    search_fields = ['course', 'course_notice', 'course_goal', 'add_time']
    list_editable = ['course_notice', 'course_goal']


class TagsAdmin:
    list_display = ['tag', 'add_time']
    list_filter = ['tag']
    search_fields = ['tag', 'add_time']
    list_editable = ['tag']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Section, SectionAdmin)
xadmin.site.register(CourseCategory, CourseCategoryAdmin)
xadmin.site.register(CourseType, CourseTypeAdmin)
xadmin.site.register(CourseAnnouncement, CourseAnnouncementAdmin)
xadmin.site.register(CourseNotice, CourseNoticeAdmin)
xadmin.site.register(Tags, TagsAdmin)

