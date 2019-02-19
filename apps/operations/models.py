# _*_ coding: utf-8 _*_

from django.db import models
from django.utils import timezone

from users.models import UserProfiles
from courses.models import Course
from organizations.models import Teacher

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名称')
    question = models.TextField(verbose_name=u'咨询内容')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'问询添加时间')

    class Meta:
        verbose_name = u'课程咨询'
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, verbose_name=u'用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u'教师')
    course_mark = models.FloatField(default=10.0, verbose_name=u'课程评分')
    teacher_mark = models.FloatField(default=10.0, verbose_name=u'教师评分')
    comment = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'问询添加时间')

    class Meta:
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name


class UserCollection(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, verbose_name=u'用户')
    # 根据数据表的 id 和收藏的类型来指定：谁的收藏数增加
    collection_id = models.IntegerField(default=0, verbose_name=u'数据表_id')
    collection_type = models.CharField(
        choices=((1, u'课程'), (2, u'课程机构'), (3, u'教师')),
        default=1, verbose_name=u'收藏类型', max_length=10
    )
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'收藏添加时间')

    class Meta:
        verbose_name = u'用户评论'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # 这里不用外键，而是使用用户的 id 来识别
    # 发给全员的消息，默认值为 0
    # 发给指定用户的消息，值指定为 用户的 id 值
    user = models.IntegerField(default=0, verbose_name=u'接受id')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'消息是否已读')
    send_time = models.DateTimeField(default=timezone.now, verbose_name=u'消息发送时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, verbose_name=u'用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'学习时间')

    class Meta:
        verbose_name = u'用户学习的课程'
        verbose_name_plural = verbose_name