# _*_ coding: utf-8 _*_

import os

from django.db import models
from django.utils import timezone

from DUEditor.models import UEditorField


# 定义动态文件的上传路径-机构图片
def get_upload_org_image_path(instance, filename):
    return os.path.join(
        'organization',
        instance.organization_name + str(instance.id),
        'organization_image',
        filename
    )


# 定义动态文件的上传路径-教师图片
def get_upload_teacher_image_path(instance, filename):
    return os.path.join(
        'organization',
        instance.organization.organization_name + str(instance.organization_id),
        'teacher_image',
        filename
    )

# 定义富文本的图片和文件上传路径-机构
def get_upload_organization_ueditor_path(instance, filename):
    return os.path.join(
        'organization',
        instance.organization_name + str(instance.id),
        'organization_description',
        filename
    )

# 定义富文本的图片和文件上传路径-教师
def get_upload_teacher_ueditor_path(instance, filename):
    return os.path.join(
        'organization',
        instance.organization.organization_name + str(instance.organization_id),
        'teacher_description',
        filename
    )



class CityDict(models.Model):
    city_name = models.CharField(max_length=20, verbose_name=u'城市名称')
    description = models.CharField(max_length=500, verbose_name=u'城市描述')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'城市添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city_name


class CourseOrganization(models.Model):
    organization_name = models.CharField(max_length=50, verbose_name=u'授课机构名称', unique=True)
    description = UEditorField(
        verbose_name=u'机构描述',
        height=400,
        width=800,
        imagePath=get_upload_organization_ueditor_path,
        filePath=get_upload_organization_ueditor_path,
        default='',
        blank=True
    )
    tag = models.CharField(default=u'全国知名', max_length=10, verbose_name=u'机构标签')
    collect_number = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    organization_image = models.ImageField(
        upload_to=get_upload_org_image_path,
        default='organization/default_images/organization_image_default.png',
        max_length=500,
        verbose_name=u'机构图片',
        blank=True
    )
    organization_type = models.CharField(
        verbose_name=u'机构类型',
        choices=(('collage', u'高校'), ('training_institution', u'培训机构'), ('personal', u'个人')),
        max_length=20
    )
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_number = models.IntegerField(default=0, verbose_name=u'机构课程数量')
    organization_mark = models.FloatField(default=10.0, verbose_name=u'机构评分')
    address = models.CharField(max_length=150, default=u'', verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u'机构所在地')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'机构添加时间')

    class Meta:
        verbose_name = u'授课机构'
        verbose_name_plural = verbose_name

    # 定义返回机构的教师数量
    def get_teacher_number(self):
        return self.teacher_set.all().count()

    # 定义返回机构的课程数量
    def get_course_number_org(self):
        return self.course_number

    # 获取机构的 2 门经典课程，以课程的收藏量为基准
    # 使用 QuerySet 对象的 union 方法合并多个 QuerySet 对象
    def get_valuable_courses(self):
        teacher_course_list = [teacher.course_teacher.all() for teacher in self.teacher_set.all()]
        # 判断 teacher_course_list 的长度，有可能机构还没有课程
        if teacher_course_list:
            valuable_course = teacher_course_list[0]
            for course in teacher_course_list[1:]:
                # 这里使用 | 操作符合并两个 QuerySet 对象
                valuable_course = valuable_course | course
            valuable_course = valuable_course.order_by('-collect_number')[:2]
            return valuable_course
        return []

    def __str__(self):
        return self.organization_name


class Teacher(models.Model):
    organization = models.ForeignKey(CourseOrganization, on_delete=models.CASCADE, verbose_name=u'所属机构')
    teacher_name = models.CharField(max_length=50, verbose_name=u'教师名称')
    description = UEditorField(
        verbose_name=u'机构描述',
        height=400,
        width=800,
        imagePath=get_upload_teacher_ueditor_path,
        filePath=get_upload_teacher_ueditor_path,
        default='',
        blank=True
    )
    teacher_mark = models.FloatField(default=10.0, verbose_name=u'教师总评分')
    inauguration_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    company_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    work_year = models.IntegerField(default=0, verbose_name=u'工作年限')
    collect_number = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    teacher_image = models.ImageField(upload_to=get_upload_teacher_image_path,
                                      default='organization/default_images/teacher_image_default.png',
                                      max_length=500, verbose_name=u'教师图片', blank=True)
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'教师添加时间')


    class Meta:
        verbose_name = u'授课讲师'
        verbose_name_plural = verbose_name

    # 获取教师的课程数量
    def get_course_number_teacher(self):
        course_number = self.course_teacher.all().count()
        return course_number
    get_course_number_teacher.short_description = u'课程数量'

    # 获取教师经典课程，以收藏量为基准
    def get_valuable_course(self):
        course = self.course_teacher.all().order_by('-collect_number')
        if course:
            return course[0]
        else:
            return ''

    def __str__(self):
        return '{}>{}'.format(self.teacher_name, self.organization.organization_name)
