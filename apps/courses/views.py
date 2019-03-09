# _*_ coding: utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
# 分页功能组件（第三方）
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q

from .models import Course, CourseResource, CourseNotice, CourseAnnouncement, Section
from organizations.models import Teacher, CourseOrganization
from operations.models import UserCollection, CourseComment, UserCourse, UserMessage
from utils.mixin_utils import LoginRequiredMixin
from users.models import UserProfiles


# 专业课的课程列表
class SpecializedCoursesList(View):
    def get(self, request):
        # 获取专业课程对象
        courses = Course.objects.filter(open_type='specialized').order_by('-add_time')
        # 以课程评价前三的课程作为热门课程（如有重复，按添加时间降序）
        hot_courses = courses.order_by('-course_mark', '-add_time')[:3]

        # 课程搜索关键字
        # 使用 django 的 ORM 中的 __icontains，它会在数据库中生成 like 的语句进行匹配
        # i 标识不区分大小写
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            courses = courses.filter(
                Q(course_name__icontains=search_keyword) |
                Q(detail__icontains=search_keyword) |
                Q(description__icontains=search_keyword)
            )

        # 页面筛选功能的实现
        sort = request.GET.get('sort', '')
        # 最热门课程（收藏数）
        if sort == 'hot':
            courses = courses.order_by('-collect_number')
        # 学习人数最多的课程
        elif sort == 'students':
            courses = courses.order_by('-student_number')

        # 获取页面传回的分页数值，默认为 1（第一页）
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对数据库中所取出的所有对象，进行分页，中间的参数为每页显示的对象个数，设置为 6 个
        p = Paginator(courses, 6, request=request)
        # 取出对应页的数据
        courses_list = p.page(page)

        return render(request, 'courses/course-list.html', {
            'courses': courses_list,
            'hot_courses': hot_courses,
            'open_type': 'specialized',
            'sort': sort,
            'focus': 'specialized',
        })


# 公开课的课程列表
class OpenCoursesList(View):
    def get(self, request):
        # 获取公开课程对象
        courses = Course.objects.filter(open_type='open').order_by('-add_time')
        # 以点击量前三的课程作为热门课程
        hot_courses = courses.order_by('-course_mark', '-add_time')[:3]

        # 课程搜索关键字
        # 使用 django 的 ORM 中的 __icontains，它会在数据库中生成 like 的语句进行匹配
        # i 标识不区分大小写
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            courses = courses.filter(
                Q(course_name__icontains=search_keyword)|
                Q(detail__icontains=search_keyword)|
                Q(description__icontains=search_keyword)
            )

        # 页面筛选功能的实现
        sort = request.GET.get('sort', '')
        # 最热门课程（收藏数）
        if sort == 'hot':
            courses = courses.order_by('-collect_number')
        # 学习人数最多的课程
        elif sort == 'students':
            courses = courses.order_by('-student_number')

        # 获取页面传回的分页数值，默认为 1（第一页）
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对数据库中所取出的所有对象，进行分页，中间的参数为每页显示的对象个数，设置为 6 个
        p = Paginator(courses, 6, request=request)
        # 取出对应页的数据
        courses_list = p.page(page)

        return render(request, 'courses/course-list.html', {
            'courses': courses_list,
            'hot_courses': hot_courses,
            'open_type': 'open',
            'sort': sort,
            'focus': 'open',
        })


# 课程详情页面
class CourseDetail(View):
    def get(self, request, course_id):
        # 通过课程的 id 从数据库中获取相应的课程信息
        course = Course.objects.filter(id=course_id)[0]

        # 点击数量加 1
        course.click_number += 1
        course.save()

        # 通过课程反向查询教师信息
        teacher = Course.objects.get(id=course_id).course_teacher
        # 通过教师信息，反向查询机构信息
        org = Teacher.objects.get(id=teacher.id).organization

        # 获取课程的标签，根据标签推荐 2 门相似课程, all() 获取所有的标签，first() 是获取第一个标签
        # tag = course.course_tag.all()
        tag = course.course_tag.all()
        if tag:
            tag = tag[0]
            # 使用 Q 对象进行 and 和 not 并集查询
            # 在 filter 中不能使用 != 来表示不等于，需用 Q 对象中的「~Q()」
            same_courses = Course.objects.filter(
                Q(course_tag=tag),
                ~Q(id=course.id)
            ).order_by('-collect_number')[:2]
        else:
            same_courses = []

        # 课程学习用户的展示
        user_studys = UserCourse.objects.filter(course_id=course_id)[:5]

        # 如果是登录的情况下
        if request.user.is_authenticated:
            # 增加用户收藏状态的判断-课程
            collection_course = UserCollection.objects.filter(
                user=request.user,
                collection_id=course.id,
                collection_type=1
            )
            if collection_course:
                is_course_collected = u'已收藏'
            else:
                is_course_collected = u'收藏'

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
            is_organization_collected = u'收藏'
            is_course_collected = u'收藏'

        if course:
            return render(request, 'courses/course-detail.html', {
                'course': course,
                'teacher': teacher,
                'org': org,
                'is_course_collected': is_course_collected,
                'is_organization_collected': is_organization_collected,
                'same_courses': same_courses,
                'user_studys': user_studys,

                # 选中状态标志
                'focus': course.open_type,
            })


# 课程学习页面
class CourseStudy(LoginRequiredMixin, View):
    def get(self, request, course_id):

        # 获取课程的内容
        course = Course.objects.get(id=course_id)
        # 获取课程的章节信息
        chapters = course.chapter_set.all()
        # 获取课程资源
        resources = CourseResource.objects.filter(course_id=course_id)

        # 获取课程公告
        course_announcement = CourseAnnouncement.objects.filter(course_id=course_id)
        if course_announcement:
            course_announcement = course_announcement[0]
        else:
            course_announcement = ''

        # 获取课程提示
        course_notice = CourseNotice.objects.filter(course_id=course_id)
        if course_notice:
            course_notice = course_notice[0]
        else:
            course_notice = ''

        # 获取课程推荐
        # 从 UserCourse 表中获取所有学过该课程的同学，得到的是一个 QuerySet 对象
        user_course = UserCourse.objects.filter(course_id=course_id)
        # 获取所有同学的 id
        user_ids = [user.user_id for user in  user_course]
        course_recommends = UserCourse.objects.filter(Q(user_id__in=user_ids), ~Q(course_id=course_id))
        if course_recommends:
            course_recommends = course_recommends[:5]
        else:
            course_recommends = []


        return render(request, 'courses/course-study.html', {
            'course': course,
            'chapters': chapters,
            'resources': resources,
            'course_announcement': course_announcement,
            'course_notice': course_notice,
            'course_recommends': course_recommends,

            # 选中状态标志
            'focus': course.open_type,
        })


# 课程评论页面
class CourseCommentView(LoginRequiredMixin, View):

    def get(self, request, course_id):

        # 获取课程评论
        comments = CourseComment.objects.filter(course_id=course_id).order_by('-add_time')
        # 获取课程的信息
        course = Course.objects.get(id=course_id)
        # 获取课程资源
        resources = CourseResource.objects.filter(course_id=course_id)
        # 获取课程公告
        course_announcement = CourseAnnouncement.objects.get(course_id=course_id)


        # 获取课程推荐
        # 从 UserCourse 表中获取所有学过该课程的同学，得到的是一个 Qset 对象
        user_course = UserCourse.objects.filter(course_id=course_id)
        # 获取所有同学的 id
        user_ids = [user.user_id for user in user_course]
        course_recommends = UserCourse.objects.filter(Q(user_id__in=user_ids), ~Q(course_id=course_id))
        if course_recommends:
            course_recommends = course_recommends[:5]
        else:
            course_recommends = []

        # 获取页面传回的分页数值，默认为 1（第一页）
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对数据库中所取出的所有对象，进行分页，中间的参数为每页显示的对象个数，设置为 6 个
        p = Paginator(comments, 1, request=request)
        # 取出对应页的数据
        comments_list = p.page(page)


        return render(request, 'courses/course-comment.html', {
            'comments': comments_list,
            'course': course,
            'resources': resources,
            'course_announcement': course_announcement,
            'course_recommends': course_recommends,

            # 选中状态标志
            'focus': course.open_type,
        })


# 添加评论
class AddCourseCommentView(LoginRequiredMixin, View):
    def post(self, request):

        # 获取评论的课程 id 和评论内容
        course_id = int(request.POST.get('course_id', 0))
        course_mark = float(request.POST.get('course_mark', 10))
        course_comment = request.POST.get('comments', '')

        # 判断用户登录状态
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': u'用户未登录'})

        # 获取用户信息
        user = request.user.id

        # 后台判断评论是否符合要求
        if not all((course_id > 0, 6 <= course_mark <= 10, course_comment)):
            return JsonResponse({'status': 'fail', 'msg': u'添加评论失败'})

        # 这里有一个问题，有没有追加评论的功能，是否允许用户多次评论
        # 暂定逻辑，用户的追加评论将修改原有的评论
        comment = CourseComment.objects.filter(course_id=course_id, user=user)
        if not comment:
            # 新建评论
            comment = CourseComment()
            comment.course_mark = course_mark
            comment.comment = course_comment
            # 由于 user 和 course 是一个外键，因此需要实例化
            comment.course = Course.objects.get(id=course_id)
            comment.user = request.user
            comment.save()
            return JsonResponse({'status': 'success', 'msg': u'评论添加成功'})
        else:
            # 修改评论
            comment = comment[0]
            comment.course_mark = course_mark
            comment.comment = course_comment
            comment.save(update_fields=['course_mark', 'comment'])
            return JsonResponse({'status': 'success', 'msg': u'评论修改成功'})


# 课程添加到用户学习表中
class AddCourseStudy(LoginRequiredMixin, View):
    def post(self, request):

        # 获取课程的 id
        course_id = request.POST.get('course_id', '')

        # 判断用户登录状态
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': u'用户未登录'})

        # 判断用户是否已经处于学习状态
        user_course = UserCourse.objects.filter(user_id=request.user.id, course_id=course_id)
        if user_course:
            return JsonResponse({'status': 'success', 'msg': u'已添加学习'})
        else:
            user_course = UserCourse()
            # 实例化一个课程对象
            course = Course.objects.get(id=course_id)
            user_course.course = course
            user_course.user = request.user
            user_course.save()

            # 点击学习，学习人数加 1
            course.student_number += 1
            course.save()

            # 课程机构的学习人加 1
            org = course.course_teacher.organization
            org.students += 1
            org.save()

            # 用户添加学习时，发送消息给用户
            user_message = UserMessage()
            user_message.user = request.user.id
            user_message.message = '欢迎你学习<{}>这门课程\n{}'.format(course.course_name,course.description)
            user_message.save()

            return JsonResponse({'status': 'success', 'msg': u'已添加学习'})


# 课程的视频播放页面
class CourseStudyDetail(LoginRequiredMixin, View):
    def get(self, request, course_id, section_id):
        # 获取课程小结
        section = Section.objects.get(id=section_id)
        # 获取课程评论
        comments = CourseComment.objects.filter(course_id=course_id).order_by('-add_time')
        # 获取课程的信息
        course = Course.objects.get(id=course_id)
        # 获取课程的章节信息
        chapters = course.chapter_set.all()
        # 获取课程资源
        resources = CourseResource.objects.filter(course_id=course_id)
        # 获取课程公告
        course_announcement = CourseAnnouncement.objects.get(course_id=course_id)
        # 获取课程提示
        course_notice = CourseNotice.objects.get(course_id=course_id)

        # 获取课程推荐
        # 从 UserCourse 表中获取所有学过该课程的同学，得到的是一个 Qset 对象
        user_course = UserCourse.objects.filter(course_id=course_id)
        # 获取所有同学的 id
        user_ids = [user.user_id for user in user_course]
        course_recommends = UserCourse.objects.filter(Q(user_id__in=user_ids), ~Q(course_id=course_id))
        if course_recommends:
            course_recommends = course_recommends[:5]
        else:
            course_recommends = []

        # 获取页面传回的分页数值，默认为 1（第一页）
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对数据库中所取出的所有对象，进行分页，中间的参数为每页显示的对象个数，设置为 6 个
        p = Paginator(comments, 1, request=request)
        # 取出对应页的数据
        comments_list = p.page(page)

        return render(request, 'courses/course-play.html', {
            'comments': comments_list,
            'course': course,
            'resources': resources,
            'chapters': chapters,
            'course_announcement': course_announcement,
            'course_notice': course_notice,
            'course_recommends': course_recommends,
            'section': section,

            # 选中状态标志
            'focus': course.open_type,
        })