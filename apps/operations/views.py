# _*_ coding: utf-8 _*_

import json
from time import sleep

from django.shortcuts import render, reverse
from django.views.generic import View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserCourse, UserCollection, UserMessage
from courses.models import Course
from organizations.models import CourseOrganization, Teacher
from users.models import UserProfiles, EmailVerifyRecord
from utils.mixin_utils import LoginRequiredMixin
from utils.email_send import send_email_verify_record
from .forms import ResetUserHeaderPortraitForm, ResetUserPasswordForm, SendEmailForm, ResetUserInformationForm


# 定义获取用户收藏的函数
def get_user_collect(user_id, collection_type):
    course_teacher_org = {
        '1': Course,
        '2': CourseOrganization,
        '3': Teacher,
    }
    collection_ids = [collection.collection_id for collection in UserCollection.objects.filter(
        user_id=user_id,
        collection_type=collection_type)]
    collections = course_teacher_org.get(str(collection_type)).objects.filter(pk__in=collection_ids)
    return collections


# 用户个人中心-用户信息
class UserCenterInformation(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'operations/usercenter-info.html', {
            'user': user,
            'focus': 'user_info',
        })


# 用户学习的课程
class UserStudyCourse(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.id

        # 获取用户学习的课程信息
        course_ids =[course.course_id for course in  UserCourse.objects.filter(user_id=user)]
        # 使用关键字 __in 来获取列表中的条件
        user_courses = Course.objects.filter(pk__in=course_ids)

        return render(request, 'operations/usercenter-mycourse.html', {
            'user_courses': user_courses,
            'focus': 'user_mycourse',
        })


# 用户消息
class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        # 获取用户消息
        user_messages = UserMessage.objects.filter(user=user.id).order_by("-send_time")
        for user_message in user_messages:
            user_message.has_read = True
            user_message.save()


        # 获取页面传回的分页数值，默认为 1（第一页）
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对数据库中所取出的所有对象，进行分页，中间的参数为每页显示的对象个数，设置为 6 个
        p = Paginator(user_messages, 6, request=request)
        # 取出对应页的数据
        user_message_list = p.page(page)

        return render(request, 'operations/usercenter-message.html', {
            'user': user,
            'user_messages': user_message_list,
            'focus': 'user_message',
        })


# 用户收藏的讲师
class UserCollectedTeacher(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        collections = get_user_collect(user_id=user, collection_type=3)

        return render(request, 'operations/usercenter-fav-teacher.html', {
            'user': user,
            'focus': 'user_fav',
            'collections': collections,
        })



# 用户收藏的课程
class UserCollectedCourse(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        collections = get_user_collect(user_id=user, collection_type=1)

        return render(request, 'operations/usercenter-fav-course.html', {
            'user': user,
            'focus': 'user_fav',
            'collections': collections,
        })


# 用户收藏的讲师
class UserCollectedOrganization(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        collections = get_user_collect(user_id=user, collection_type=2)

        return render(request, 'operations/usercenter-fav-org.html', {
            'user': user,
            'focus': 'user_fav',
            'collections': collections,
        })


# 修改用户头像
class ResetUserHeaderPortraitView(LoginRequiredMixin, View):
    def post(self, request):
        # request 对象中有一个 FILES 对象，相应中携带的文件保存在这里
        head_portrait_form = ResetUserHeaderPortraitForm(request.POST, request.FILES, instance=request.user)
        if head_portrait_form.is_valid():
            request.user.save()
            return JsonResponse({'static': 'success'})
        else:
            return JsonResponse({'static': 'fail'})


# 修改用户密码
class ResetUserPasswordView(View):
    def post(self, request):
        password_form = ResetUserPasswordForm(request.POST)
        if password_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return JsonResponse({'status': 'fail', 'msg': u'两次输入的密码不一致'})
            user = request.user
            user.password = make_password(password1)
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            # 这里一定要加上这个参数 safe=False
            # 这样如果传入的不是正常的字典，也可以返回
            # 否则会报错 TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False.
            # result = json.dumps(password_form.errors)
            # return JsonResponse(result, safe=False)
            # 这里直接使用 JsonResponse 有问题，传入的错误信息，前端无法显示
            return HttpResponse(json.dumps(password_form.errors), content_type='application/json')


# 修改用户邮箱
class SendEmailView(View):
    def get(self, request):
        email_form = SendEmailForm(request.GET)

        if email_form.is_valid():
            # 获取用户填入的邮箱，并进行唯一性验证，如果是已经注册过的邮箱，返回错误信息
            new_email = request.GET.get('email')
            exist_email = UserProfiles.objects.filter(email=new_email)
            if exist_email:
                return JsonResponse({'email': u'该邮箱已被注册'})

            # 发送修改邮箱的邮件验证码
            send_status = send_email_verify_record(new_email, 'reset_email')
            # 验证是否发送成功，如果送失败，重发三次，如果还是失败，删除用户数据，提示用户重新注册

            if not send_status:
                resend_status = False
                for times in range(3):
                    resend_status = send_email_verify_record(new_email, 'reset_email')
                    if resend_status:
                        break
                if not resend_status:
                    return JsonResponse({'status':'fail', 'msg': u'邮件发送失败，请稍后再试'})

            # 邮件发送成功
            return JsonResponse({'status':'success', 'msg': u'邮件发送成功'})

        # 邮件格式验证错误
        return JsonResponse({'status': 'fail', 'msg': u'邮箱格式不合规'})


class ResetUserEmailView(View):
    def post(self, request):
        # 获取前端传回的信息
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        # 进入数据库库验证邮件验证码
        email_verify = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='reset_email')
        if email_verify:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'fail', 'email': u'验证码错误'})


# 修改用户信息
class ResetUserInformationView(View):
    def post(self, request):
        user_info_form = ResetUserInformationForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            request.user.save()
            return JsonResponse({'status':'success'})
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 读取用户消息
class ReadMessageView(View):
    def post(self, request):
        pass