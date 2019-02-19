# _*_ coding: utf-8 _*_

from django.db import models
from django.utils import timezone


class CityDict(models.Model):
    city_name = models.CharField(max_length=20, verbose_name=u'城市名称')
    description = models.CharField(max_length=500, verbose_name=u'城市描述')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'城市添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name


class CourseOrganization(models.Model):
    organization_name = models.CharField(max_length=50, verbose_name=u'授课机构名称')
    description = models.TextField(verbose_name=u'机构描述')
    collect_number = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    organization_image = models.ImageField(upload_to='organizations/static/organizations/image/organization/%Y/%m',
                                     max_length=500, verbose_name=u'机构图片')
    address = models.CharField(max_length=150, default=u'', verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u'机构所在地')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'机构添加时间')

    class Meta:
        verbose_name = u'授课机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    organization = models.ForeignKey(CourseOrganization, on_delete=models.CASCADE, verbose_name=u'所属机构')
    teacher_name = models.CharField(max_length=50, verbose_name=u'教师名称')
    description = models.TextField(verbose_name=u'教师描述')
    teacher_mark = models.FloatField(default=10.0, verbose_name=u'教师总评分')
    inauguration_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    company_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    work_year = models.IntegerField(default=0, verbose_name=u'工作年限')
    collect_number = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    teacher_image = models.ImageField(upload_to='organizations/static/organizations/image/teacher/%Y/%m',
                                      max_length=500, verbose_name=u'教师图片')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'教师添加时间')

    class Meta:
        verbose_name = u'授课讲师'
        verbose_name_plural = verbose_name