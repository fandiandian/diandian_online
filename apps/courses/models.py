# _*_ coding: utf-8 _*_

import os

from django.db import models
from django.utils import timezone
from DUEditor.models import UEditorField

from organizations.models import CourseOrganization, Teacher



# 定义动态文件的上传路径-章节
def get_upload_section_path(instance, filename):
    return os.path.join(
        'course',
        instance.chapter.course.course_name + str(instance.chapter.course_id),
        'section_content',
        instance.chapter.chapter_name,
        filename
    )


# 定义动态文件的上传路径-课程资源
def get_upload_course_resource_path(instance, filename):
    return os.path.join(
        'course',
        instance.course.course_name + str(instance.course_id),
        'course_resource',
        filename
    )


# 定义动态文件的上传路径-课程图片
def get_upload_course_image_path(instance, filename):
    return os.path.join(
        'course',
        instance.course_name + str(instance.id),
        'course_image',
        filename
    )

# 定义富文本的图片和文件上传路径-课程
def get_upload_course_ueditor_path(instance, filename):
    return os.path.join(
        'course',
        instance.course_name + str(instance.id),
        'course_description',
        filename
    )



# 定义函数，获取机构的当前的所有教师
def get_org_teachers(instance):
    teachers = CourseOrganization.objects.get(id=instance.organization_id).teacher_set.all()
    teacher_tuple = tuple([(teacher.id, teacher.teacher_name) for teacher in teachers])
    return teacher_tuple



# 课程大类模型
class CourseCategory(models.Model):
    course_category = models.CharField(max_length=20, verbose_name=u'课程大类')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程大类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_category


# 课程小类模型
class CourseType(models.Model):
    course_type = models.CharField(max_length=20, verbose_name=u'课程小类')
    course_category = models.ForeignKey(
        CourseCategory,
        on_delete=models.CASCADE,
        verbose_name=u'课程小类所属的大类'
    )
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程小类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_type


# 课程标签
class Tags(models.Model):
    tag = models.CharField(max_length=10, verbose_name=u'标签')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


# 课程模型
class Course(models.Model):
    course_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name=u'课程教师',
        related_name='course_teacher'
    )
    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.CASCADE,
        verbose_name=u'课程小类'
    )
    course_name = models.CharField(max_length=30, verbose_name=u'课程名称')
    description = models.TextField(max_length=50, verbose_name=u'课程描述')
    detail = UEditorField(
        verbose_name=u'课程详情',
        height=400,
        width=800,
        imagePath=get_upload_course_ueditor_path,
        filePath=get_upload_course_ueditor_path,
        default='',
        blank=True
    )
    degree = models.CharField(max_length=10, verbose_name=u'课程难度',
                              choices=(('easy', u'初级'), ('normal', u'中级'), ('hard', u'高级')))
    is_banner = models.CharField(
        choices=(('False', u'否'), ('True', u'是')),
        default='False',
        verbose_name=u'是否处于轮播位',
        max_length=10
    )
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    student_number = models.IntegerField(default=0, verbose_name=u'学习人数')
    collect_number = models.IntegerField(default=0, verbose_name=u'收藏人数')
    course_mark = models.FloatField(default=10.0, verbose_name=u'课程评分')
    course_image = models.ImageField(
        upload_to=get_upload_course_image_path,
        default='course/default_image/course_default.jpg',
        max_length=500,
        verbose_name=u'课程图片',
        blank=True
    )
    open_type = models.CharField(max_length=20, verbose_name=u'课程类型', default='open',
                                   choices=(('open', u'公开课'), ('specialized', u'专业课')))
    # 点击量不同于学习人数，用于统计点击/学习转化比，每次点开一次课程，点击量加 1
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    # 课程标签与课程的关系式 多对多
    course_tag = models.ManyToManyField(Tags, blank=True, verbose_name=u'标签')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'课程添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_name


# 定义轮播课程，继承自课程
class BannerCourse(Course):

    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


# 章节模型
class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名称', on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'章节添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0} > {1}'.format(self.course, self.chapter_name)


# 小结模型
class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name=u'章节名')
    section_name = models.CharField(max_length=100, verbose_name=u'小节名称')
    section_content = models.FileField(
        upload_to=get_upload_section_path,
        verbose_name=u'课程小结内容文件',
        default=u''
    )
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'小节添加时间')

    class Meta:
        verbose_name = u'小节'
        verbose_name_plural = verbose_name


# 课程资源模型
class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程相关资源')
    resource_name = models.CharField(max_length=50, verbose_name=u'资源名称')
    download = models.FileField(upload_to=get_upload_course_resource_path,
                                max_length=200, verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'资源添加时间')

    class Meta:
        verbose_name = u'课程相关资源'
        verbose_name_plural = verbose_name


# 课程公告
class CourseAnnouncement(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, verbose_name=u'关联课程')
    course_announcement = models.CharField(max_length=200, verbose_name=u'课程公告', default=u'')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程公告'
        verbose_name_plural = verbose_name


# 课程提示
class CourseNotice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'关联课程')
    course_notice = models.CharField(max_length=200, verbose_name=u'课程基础', default=u'')
    course_goal = models.CharField(max_length=200, verbose_name=u'课程目标', default=u'')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程须知'
        verbose_name_plural = verbose_name

