# _*_ coding: utf-8 _*_

from django.shortcuts import render
from django.urls import reverse
# django 自带的账户认证方法「authenticate」和登录方法「login」
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
# 导入 django 自带的用户认证模版
from django.contrib.auth.backends import ModelBackend
# 导入 django 自带的数据库查询类
from django.db.models import Q
# 导入 django 自带的视图基类
from django.views.generic.base import View
# 导入 django 自带的密码加密函数
from django.contrib.auth.hashers import make_password

from users.models import UserProfiles, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
# 导入自定义的邮件发送模块，实现邮件的发送
from utils.email_send import send_email_verify_record


# 自定义登录验证方式，实现用户名，邮箱，手机均可登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用「Q」类实现「并集」查询
            user = UserProfiles.objects.get(Q(username=username)|Q(email=username)|Q(mobile=username))
            # 调用「UserProfiles」继承的方法「check_password」，将传入的明文密码进行加密，并与数据库中的密文密码进行对比
            # 如果对比成功，则验证通过，返回「user」，对比失败或者出现异常，则返回「None」
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 使用类来实现用户登录功能
class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html', {})

    def post(self, request):
        # 这里会的「login_form」实例会自动从「request.POST」获取相应的字段值
        # 所以「LoginForm」中定义的「键名」一定要和「html」页面中「form」标签提交的「键名」对应起来，否则会获取失败
        login_form = LoginForm(request.POST)
        # 「is_valid()」检查「login_form」实例中的「_errors」是否为空，如果为空，则验证成功
        # 「_error」是一个字典表
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            # 如果未通过验证，user == None
            if user:
                # 验证用户是否已激活，如果未激活，则重新跳转登录页面，给出提示信息
                if user.is_active:
                    # 这里「login函数」会对「request请求作出一些更改」
                    login(request, user)
                    # 重定向到登录后的主页
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'users/login.html', {'msg': u'用户未激活，请前往注册邮箱点击激活链接完成激活'})
            else:
                # 返回「帐号验证」的错误信息
                return render(request, 'users/login.html', {'msg': u'帐号或密码错误'})
        else:
            # 返回「表单验证」的错误信息
            return render(request, 'users/login.html', {'login_form': login_form})


# # 返回主页
# def index(request):
#     return render(request, 'index.html')

# 返回登录页面，（由于使用类登录，此处的代码不再需要，注释掉）
# def user_login(request):
#     # 每个「HTTP请求」都有一个请求类型，一般是「GET」和「POST」
#     # 「POST」方法是通过「HTTP」发送的，更加完全，没有长度限制，地址栏中不可见
#     # 「GET」方法是经过编码后，通过「URL」发送，可以在地址栏中看到，发送的数据一般不能大于2kb
#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=password)
#         # 如果未通过验证，user == None
#         if user:
#             # 这里「login函数」会对「request请求作出一些更改」
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': u'帐号或密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})


# 实现用户的登出，并重定向到主页
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        # 这里不需要填入参数：request.POST,只是用于生成验证码的图片
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user_email = request.POST.get('email', '')
            if UserProfiles.objects.filter(username=user_name):
                return render(request, 'users/register.html',
                              {'msg_username_error': u'用户名已被注册，请更换用户名', 'register_form': register_form})
            if UserProfiles.objects.filter(email=user_email):
                return render(request, 'users/register.html',
                              {'msg_email_error': u'邮箱已被注册，请更换邮箱', 'register_form': register_form})
            user_profile = UserProfiles()
            user_profile.username = user_name
            user_profile.email = user_email
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            # 发送邮件验证码，获取发送状态，发送失败为 False
            send_status = send_email_verify_record(user_name, user_email, 'register')
            # 验证是否发送成功，如果送失败，重发三次，如果还是失败，删除用户数据，提示用户重新注册
            if not send_status:
                resend_status = False
                for times in range(3):
                    resend_status = send_email_verify_record(user_email, 'register')
                    if resend_status:
                        break
                if not resend_status:
                    UserProfiles.objects.filter(username=user_name).delete()
                    return render(request, 'users/register.html',
                                  {'msg_email_send_error': u'抱歉，验证邮件多次发送失败，请重新进行注册',
                                   'register_form': register_form})

            return render(request, 'users/login.html', {})
        else:
            return render(request, 'users/register.html', {'register_form': register_form})


# 邮箱验证码的验证过程
# 通过发送邮件的方式将系统生成的随机验证码附带到链接中
# 后台解析「url」链接获取验证码，进入邮件验证码的数据表对比
# 如果通过验证，将用户信息中的「is_active」改为「True」，并返回登录页面
class ActiveCode(View):
    def get(self, request, active_code):
        email_verify_record = EmailVerifyRecord.objects.filter(code=active_code)
        if email_verify_record:
            email = email_verify_record[0].email
            user = UserProfiles.objects.get(email=email)
            user.is_active = True
            user.save()

            return render(request, 'users/login.html', {})


class ForgetPassWordCode(View):
    def get(self, request, user_name, forget_password_code):
        email_verify_record = EmailVerifyRecord.objects.filter(code=forget_password_code)
        if email_verify_record:
            # 验证码只能使用1次，使用后后台删除
            email_verify_record[0].delete()

            reset_password_form = ResetPasswordForm()

            return render(request, 'users/forgetpwd.html',{'reset_password_form': reset_password_form,
                                                           'msg_type': True, 'user_name': user_name})

        # 验证链接错误或已失效，重新发起验证
        else:
            forget_password_form = ForgetPasswordForm()
            return render(request, 'users/forgetpwd.html',
                          {'forget_password_form': forget_password_form,
                           'msg_type': False, 'msg_failure': u'验证链接错误或已失效，需重置'})


class ForgetPassword(View):
    def get(self, request):
        forget_password_form = ForgetPasswordForm()
        return render(request, 'users/forgetpwd.html',
                      {'forget_password_form': forget_password_form,
                       'msg_type': False})

    def post(self, request):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_name = request.POST.get('username', '')
            user_email = request.POST.get('email', '')
            user = UserProfiles.objects.filter(username=user_name, email=user_email)
            if user:
                send_status = send_email_verify_record(user_name, user_email, 'forget')

                if not send_status:
                    resend_status = False
                    for times in range(3):
                        resend_status = send_email_verify_record(user_name, user_email, 'register')
                        if resend_status:
                            break
                    if not resend_status:
                        UserProfiles.objects.filter(username=user_name).delete()

                        # 邮件发送失败，跳转找回密码页面，给出提示信息
                        return render(request, 'users/forgetpwd.html',
                                      {'msg_email_send_error': u'抱歉，验证邮件多次发送失败，请重新试',
                                       'forget_password_form': forget_password_form})

                # 邮件发送成功，跳转找回密码页面，给出提示信息
                return render(request, 'users/forgetpwd.html',
                              {'msg_type': False, 'msg_send_successful': u'验证链接已发送至你的邮箱，请前往邮箱完成验证'})

            # 用户名和邮箱联合查询失败，跳转找回密码页面，给出提示信息
            return render(request, 'users/forgetpwd.html',
                          {'forget_password_form': forget_password_form,
                           'msg_username_error': u'用户名与邮箱不匹配，请重新输入', 'msg_type': False})

        # 表单填写不合规，跳转找回密码页面，给出提示信息
        return render(request, 'users/forgetpwd.html',
                      {'forget_password_form': forget_password_form, 'msg_type': False})


class ResetPassword(View):
    def post(self, request):
        reset_password_form = ResetPasswordForm(request.POST)
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        user_name = request.POST.get('username', '')
        if password != password2:
            return render(request, 'users/forgetpwd.html', {'msg_type': True, 'user_name': user_name,
                          'reset_password_form': reset_password_form,
                          'msg_equal_error': u'两次输入的密码一致，请重新输入'})

        user = UserProfiles.objects.filter(username=user_name)[0]
        user.password = make_password(password)
        user.save()
        # 完成重置，跳转登录页面
        return render(request, 'users/login.html', {})