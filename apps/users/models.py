# _*_ coding: utf-8 _*_

# 这里导入 python 内建库
import os

# 这里导入 python 第三方库
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# 这里导入自定义库


# 定义动态文件的上传路径-用户图片
def get_upload_user_image_path(instance, filename):
    return os.path.join(
        'user',
        instance.username + str(instance.id),
        'head_portrait',
        filename
    )


# 定义动态文件的上传路径-首页轮播图
def get_upload_view_page_path(instance, filename):
    return os.path.join(
        'view_page',
        instance.title + str(instance.id),
        filename
    )


class UserProfiles(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    # 用户在创建是允许不用填写此项，所以设置 null=True, blank=True
    # blank：与验证相关。当调用form.is_valid（）时，它将在表单验证期间使用。
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(choices=((u'male', u'男'), (u'female', u'女')),
                              default=u'male', verbose_name=u'性别', max_length=6)
    address = models.CharField(max_length=150, default=u'', verbose_name=u'地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'手机')
    head_portrait = models.ImageField(
        upload_to=get_upload_user_image_path,
        default='user/default_head_portrait/default.png',
        max_length=200,
        verbose_name=u'头像',
        blank=True,
    )

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    # 获取用户的未读消息数量
    def get_user_unread_messages(self):
        # 这里导入消息的模块。用户消息的模块的导入语句一定要放置在这里
        # 因为 operators.models 中导入 UserProfiles，会形成循环导入出错
        from operations.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

    def __str__(self):
        return self.username


# 底层的相对独立的模型放置的 users 中
# 邮件验证模型 和 首页轮播模型
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    # choices 函数的用途：在后台管理系统中，只能通过选择提供的值，而不能输入
    send_type = models.CharField(
        choices=(('register', u'注册'), ('forget', u'找回密码'), ('reset_email', u'重置邮箱')),
        max_length=20,
        verbose_name=u'验证码类型'
    )
    # 这里要主要，timezone.now 不能加括号，如果不去掉括号，默认值会设定为 model 编译的时间进行设定
    # 去除后，会在 EmailVerifyRecord 类实例化的时候给出默认值
    verified_times = models.IntegerField(default=3)
    send_time = models.DateTimeField(default=timezone.now, verbose_name=u'发送时间')


    class Meta:
        verbose_name = u'邮件验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0} > ({1})'.format(self.email, self.code)


class ViewPage(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'标题')
    image = models.ImageField(
        upload_to=get_upload_view_page_path,
        verbose_name=u'轮播图',
        max_length=500
    )
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u'添加时间')
    index = models.IntegerField(default=100, verbose_name=u'顺序')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
