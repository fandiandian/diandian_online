# _*_ coding: utf-8 _*_

import re

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

# 分页功能组件（第三方）
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrganization, CityDict, Teacher
from courses.models import Course
from .forms import UserAskForm
from operations.models import UserCollection, UserMessage



# 定义增加或取消收藏
def add_or_cancel_collection(type, collection_id, collection_type):
    id = {
        '1': Course,
        '2': CourseOrganization,
        '3': Teacher,
    }
    model_instance = id.get(str(collection_type))
    model_instance = model_instance.objects.get(id=collection_id)
    if type == 'add':
        model_instance.collect_number += 1
        model_instance.save()
    elif type == 'cancel':
        model_instance.collect_number -= 1
        if model_instance.collect_number < 0:
            model_instance.collect_number = 0
        model_instance.save()


# 定义用户收藏，添加收藏消息到用户消息表中
def add_collection_message_to_user_message(user_id, collection_id, collection_type):
    id = {
        '1': Course,
        '2': CourseOrganization,
        '3': Teacher,
    }
    model_instance = id.get(str(collection_type))
    model_instance = model_instance.objects.get(id=collection_id)
    user_message = UserMessage()
    user_message.user = user_id
    name = ''
    if collection_type == 1:
        name = model_instance.course_name
    elif collection_type == 2:
        name = model_instance.organization_name
    elif collection_type == 3:
        name = model_instance.teacher_name

    user_message.message = "欢迎你收藏<{}\n{}>".format(name, model_instance.description)
    user_message.save()


# 课程机构列表
class OrganizationsList(View):
    def get(self, request):
        # 获取所有的培训机构数据和城市数据
        all_orgs = CourseOrganization.objects.all().order_by('-collect_number')
        all_citys = CityDict.objects.all()
        # 获取 3 家热门机构，以收藏数为准
        hot_args = all_orgs[:3]

        # 课程搜索关键字
        # 使用 django 的 ORM 中的 __icontains，它会在数据库中生成 like 的语句进行匹配
        # i 标识不区分大小写
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_orgs = all_orgs.filter(
                Q(organization_name__icontains=search_keyword) |
                Q(description__icontains=search_keyword)|
                Q(city__city_name__icontains=search_keyword)
            )

        # 页面数据筛选
        # 获取培训机构类型筛选数据
        org_type = request.GET.get('ct', '')
        if org_type:
            all_orgs = all_orgs.filter(organization_type=org_type)

        # 获取培训机构地址筛选数据
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        count = all_orgs.count()

        # 机构排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_number')

        # 实现分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 6, request=request)

        org_list = p.page(page)

        return render(request, 'organizations/org-list.html', {
            'all_orgs': org_list,
            'all_citys': all_citys,
            'city_id': city_id,
            'org_type': org_type,
            'count': count,
            'sort': sort,
            'hot_orgs': hot_args,
            'focus': 'organization'
        })


# 用户添加问询
class AddUserAsk(View):
    # 异步操作，不刷新页面，返回的是 JsonResponse
    # 使用「form」表单搭配「js」中的「ajax」来实现
    # 「ajax」使用时会出现「403」错误，通过官方提供的方法已解决，可查看「base.html」中的说明
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            response = {'status': 'fail', 'msg': '信息填写有误，请重新填写'}
            # response = {'status': 'fail', 'msg': '{0}'.format(user_ask_form.errors)}
            return JsonResponse(response)


class OrganizationHomePage(View):
    """
    机构首页
    """
    def get(self, request, org_id):

        # 通过机构的 主键id 从机构数据表中获取机构的相关数据
        org_info = CourseOrganization.objects.get(id=org_id)

        # 进入机构，机构的点击数加 1
        org_info.click_number += 1
        org_info.save()

        # 通过机构的数据，在课程数据表中获取该机构的所有课程
        # 使用 __in 方式查询存在于一个list范围内的所有值
        courses = Course.objects.filter(
            course_teacher__in=[teacher.id for teacher in org_info.teacher_set.all()]
        ).order_by('-collect_number')[:3]
        # 机构的id 在教师数据表中获取教师的信息
        teachers = Teacher.objects.filter(organization_id=org_id).order_by('-collect_number')[:3]
        # 简版的机构简介
        description = org_info.description[:200]

        if request.user.is_authenticated:
            # 增加用户收藏状态的判断
            collection = UserCollection.objects.filter(user = request.user, collection_id=org_id, collection_type=2)
            if collection:
                is_collected = u'已收藏'
            else:
                is_collected = u'收藏'
        else:
            is_collected = u'收藏'

        return render(request, 'organizations/org-detail-homepage.html', {
            'org_info': org_info,
            'courses': courses,
            'teachers': teachers,
            'org_id': org_id,
            'description': description,
            'is_collected': is_collected,
            # 选中项变色
            'left_focus': 'home',
            'focus': 'organization',
        })


class OrganizationCoursePage(View):
    """
    机构课程
    """
    def get(self, request, org_id):
        # 通过机构的 主键 id 从机构数据表中获取机构的相关数据
        org_info = CourseOrganization.objects.get(id=org_id)
        # 通过机构的数据，在课程数据表中获取该机构的所有课程
        courses = Course.objects.filter(
            course_teacher__in=[teacher.id for teacher in org_info.teacher_set.all()]
        ).order_by('-collect_number')

        if request.user.is_authenticated:
            # 增加用户收藏状态的判断
            collection = UserCollection.objects.filter(user=request.user, collection_id=org_id, collection_type=2)
            if collection:
                is_collected = u'已收藏'
            else:
                is_collected = u'收藏'
        else:
            is_collected = u'收藏'

        # 实现分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, 6, request=request)

        courses_list = p.page(page)

        return render(request, 'organizations/org-detail-courses.html', {
            'org_info': org_info,
            'courses': courses_list,
            'org_id': org_id,
            'is_collected': is_collected,
            # 选中项变色
            'left_focus': 'course',
            'focus': 'organization',
        })


class OrganizationTeacherPage(View):
    """
    机构教师
    """
    def get(self, request, org_id):
        # 通过机构的 主键id 从机构数据表中获取机构的相关数据
        org_info = CourseOrganization.objects.filter(id=org_id)[0]
        # 机构的id 在教师数据表中获取教师的信息
        teachers = Teacher.objects.filter(organization_id=org_id).order_by('-collect_number')

        if request.user.is_authenticated:
            # 增加用户收藏状态的判断
            collection = UserCollection.objects.filter(user=request.user, collection_id=org_id, collection_type=2)
            if collection:
                is_collected = u'已收藏'
            else:
                is_collected = u'收藏'
        else:
            is_collected = u'收藏'

        # 实现分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teachers, 6, request=request)

        teachers_list = p.page(page)

        return render(request, 'organizations/org-detail-teachers.html', {
            'org_info': org_info,
            'teachers': teachers_list,
            'org_id': org_id,
            'is_collected': is_collected,
            # 选中项变色
            'left_focus': 'teacher',
            'focus': 'organization',
        })

class OrganizationDescripthionPage(View):
    """
    机构描述
    """
    def get(self, request, org_id):
        # 通过机构的 主键id 从机构数据表中获取机构的相关数据
        org_info = CourseOrganization.objects.filter(id=org_id)[0]

        if request.user.is_authenticated:
            # 增加用户收藏状态的判断
            collection = UserCollection.objects.filter(user=request.user, collection_id=org_id, collection_type=2)
            if collection:
                is_collected = u'已收藏'
            else:
                is_collected = u'收藏'
        else:
            is_collected = u'收藏'

        return render(request, 'organizations/org-detail-desc.html', {
            'org_info': org_info,
            'org_id': org_id,
            'is_collected': is_collected,
            # 选中项变色
            'left_focus': 'description',
            'focus': 'organization',
        })


class AddCollection(View):
    """
    用户收藏或取消收藏
    """
    def post(self, request):
        # 获取收藏类型和所要添加到数据表的id
        collection_id = int(request.POST.get('fav_id', 0))
        collection_type = int(request.POST.get('fav_type', 0))

        # 判断用户的登录状态
        # request 对象中有一个 user 中有一个属性 is_authenticated，如果是处于未登录状态，值是 False
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': u'用户未登录'})

        # 进入数据库查找用户的收藏记录
        exist_records = UserCollection.objects.filter(
            user=request.user,
            collection_id=collection_id,
            collection_type=collection_type
        )
        if exist_records:
            # 如果为True，记录已存在，则是用户取消收藏，执行删除操作，
            # 相应的课程或机构或教师的收藏数减 1
            add_or_cancel_collection('cancel', collection_id, collection_type)
            exist_records.delete()
            return JsonResponse({'status': 'success', 'msg': u'收藏'})
        else:
            user_collection = UserCollection()
            if collection_id > 0 and collection_type > 0:
                # 这里的 user_collection.user 直接取 request.user
                # 要求的是一个 UserProfiles 对象，登录状态在，返回的就是 UserProfiles
                # 如果用 UserProfiles 对象中属性值，会出现错误
                user_collection.user = request.user
                user_collection.collection_id = collection_id
                user_collection.collection_type = collection_type
                user_collection.save()
                add_or_cancel_collection('add', collection_id, collection_type)

                # 用户收藏时，给用户发出收藏消息
                add_collection_message_to_user_message(request.user.id, collection_id, collection_type)

                return JsonResponse({'status': 'success', 'msg': u'已收藏'})
            else:
                return JsonResponse({'status': 'fail', 'msg': u'收藏错误'})


# 教师列表
class TeacherList(View):
    def get(self, request):

        # 获取所有的教师信息
        all_teachers = Teacher.objects.all().order_by('-teacher_mark')
        # 获取热门讲师 3 位，以收藏量为基准
        hot_teachers = all_teachers.order_by('-collect_number')[:3]

        # 课程搜索关键字
        # 使用 django 的 ORM 中的 __icontains，它会在数据库中生成 like 的语句进行匹配
        # i 标识不区分大小写
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_teachers = all_teachers.filter(
                Q(teacher_name__icontains=search_keyword) |
                Q(description__icontains=search_keyword)
            )

        # 筛选功能
        sort = request.GET.get('sort', '')
        if sort:
            all_teachers = all_teachers.order_by('-collect_number')

        # 教师人数统计
        count = all_teachers.count()

        # 实现分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 6, request=request)

        teachers_list = p.page(page)

        return render(request, 'organizations/teachers-list.html', {
            'all_teachers': teachers_list,
            'hot_teachers': hot_teachers,
            'count': count,
            'sort': sort,
            # 选中项变色
            'focus': 'teacher',
        })


# 教师详情
class TeacherInformation(View):
    def get(self, request, teacher_id):

        # 根据请求中附带的 teacher_id 进入数据库中查询教师信息
        teacher = Teacher.objects.get(id=teacher_id)

        # 进入教师详情页面，教师的点击数加 1
        teacher.click_number += 1
        teacher.save()

        # 获取热门教师3位
        hot_teachers = Teacher.objects.order_by('-collect_number')[:3]

        # 获取教师的全部课程，以添加时间为基准
        courses = Course.objects.filter(course_teacher=teacher).order_by('-add_time')
        # 热门课程筛选，以收藏数为基准
        sort = request.GET.get('sort', '')
        if sort:
            courses = courses.order_by('-collect_number')

        if request.user.is_authenticated:
            # 增加用户收藏状态的判断-教师
            collection_teacher = UserCollection.objects.filter(user=request.user, collection_id=teacher.id, collection_type=3)
            if collection_teacher:
                is_teacher_collected = u'已收藏'
            else:
                is_teacher_collected = u'收藏'
            # 增加用户收藏状态的判断-机构
            collection_organization = UserCollection.objects.filter(
                user=request.user,
                collection_id=teacher.organization.id,
                collection_type=2
            )
            if collection_organization:
                is_organization_collected = u'已收藏'
            else:
                is_organization_collected = u'收藏'
        else:
            is_teacher_collected = u'收藏'
            is_organization_collected = u'收藏'


        # 实现分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, 6, request=request)

        courses_list = p.page(page)

        return render(request, 'organizations/teacher-detail.html', {
            'teacher': teacher,
            'courses': courses_list,
            'hot_teachers': hot_teachers,
            'sort': sort,
            'is_teacher_collected': is_teacher_collected,
            'is_organization_collected': is_organization_collected,
            # 选中项变色
            'focus': 'teacher',
        })

