# _*_ coding: utf-8 _*_

from django.db import models
from django.utils import timezone

from users.models import UserProfiles
from courses.models import Course
from organizations.models import Teacher, CourseOrganization

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名称')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'问询添加时间')

    class Meta:
        verbose_name = u'课程咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}-{}'.format(self.name, self.course_name)


class CourseComment(models.Model):
    user = models.ForeignKey(
        UserProfiles,
        on_delete=models.CASCADE,
        verbose_name=u'用户',
        related_name='course_comment'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    course_mark = models.FloatField(default=10.0, verbose_name=u'课程评分')
    comment = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}对课程的评论'.format(self.user.username)


class TeacherComment(models.Model):
    user = models.ForeignKey(
        UserProfiles,
        on_delete=models.CASCADE,
        verbose_name=u'用户',
        related_name='teacher_comment'
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=u'教师')
    teacher_mark = models.FloatField(default=10.0, verbose_name=u'教师评分')
    comment = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}对教师的评论'.format(self.user.username)


class OrganizationComment(models.Model):
    user = models.ForeignKey(
        UserProfiles,
        on_delete=models.CASCADE,
        verbose_name=u'用户',
        related_name='organization_comment'
    )
    organization = models.ForeignKey(CourseOrganization, on_delete=models.CASCADE, verbose_name=u'机构')
    organization_mark = models.FloatField(default=10.0, verbose_name=u'机构评分')
    comment = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'机构评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}对机构的评论'.format(self.user.username)


class UserCollection(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE, verbose_name=u'用户')
    # 根据数据表的 id 和收藏的类型来指定：谁的收藏数增加
    collection_id = models.IntegerField(default=0, verbose_name=u'被收藏对象的id')
    collection_type = models.CharField(
        choices=((1, u'课程'), (2, u'课程机构'), (3, u'教师')),
        default=1, verbose_name=u'收藏类型', max_length=10
    )
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'收藏添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


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