# _*_ coding: utf-8 _*_

from django.db import models
from django.utils import timezone

class Course(models.Model):
    course_name = models.CharField(max_length=50, verbose_name=u'课程名称')
    description = models.TextField(max_length=500, verbose_name=u'课程描述')
    detail = models.TextField( verbose_name='课程详情')
    degree = models.CharField(max_length=10, verbose_name=u'课程难度',
                              choices=(('easy', u'初级'), ('normal', u'中级'), ('hard', u'高级')))
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    student_number = models.IntegerField(default=0, verbose_name=u'学习人数')
    collect_number = models.IntegerField(default=0, verbose_name=u'收藏人数')
    course_mark = models.FloatField(default=10.0, verbose_name=u'课程总评分')
    course_image = models.ImageField(upload_to='courses/static/courses/image/%Y/%m',
                                     max_length=500, verbose_name=u'课程图片')
    # 点击量不同于学习人数，用于统计点击/学习转化比，每次点开一次课程，点击量加 1
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'课程添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course_name


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'章节名称', on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'章节添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name


class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name=u'小节名称')
    lesson_name = models.CharField(max_length=100, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'小节添加时间')

    class Meta:
        verbose_name = u'小节'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程相关资源')
    resource_name = models.CharField(max_length=50, verbose_name=u'资源名称')
    download = models.FileField(upload_to='courses/static/courses/resource/%Y/%m',
                                max_length=200, verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'资源添加时间')

    class Meta:
        verbose_name = u'课程相关资源'
        verbose_name_plural = verbose_name