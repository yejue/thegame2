import logging
from django.shortcuts import render
from django.views import View

from .forms import RegisterForm, LoginForm
from .models import User

from utils.genJsonResponse import json_response
from utils.res_code import *
from utils.getUserMeta import get_ip

# Create your views here.

logger = logging.getLogger('thegame')
logger2 = logging.getLogger('django')


class ThecodeView(View):
    """
    入口页视图
    url:thecode/
    """
    def get(self, request):
        logger2.info('有人访问 {}'.format(get_ip(request)))
        return render(self.request, "thecode/thecode.html")

    def post(self, request):
        # 校验数据
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            return json_response(errno=Code.OK, errmsg='登录成功')
        else:
            # 将表单错误信息进行拼接
            err_msg_str = '/'.join([item[0] for item in form.errors.values()])
            return json_response(errno=Code.PARAMERR, errmsg=err_msg_str)


class CommentsView(View):
    """
    活动解释页
    url:thecode/comments
    """
    def get(self, request):
        return render(self.request, "thecode/comments.html")


class GetURL(View):
    """
    返回url
    url:thecode/url=register
    """
    def get(self, request, tag):
        if tag == "register":
            data = {
                "url": "/thecode/098f6bcd4621d373cade4e832627b4f6"
            }
            return json_response(data=data)
        return json_response(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])


class RegisterView(View):
    """
    注册视图
    url: thecode/098f6bcd4621d373cade4e832627b4f6
    """
    def get(self, request):
        return render(request, "thecode/register.html")

    def post(self, request):
        # 1.校验数据
        form = RegisterForm(request.POST, request=request)
        if form.is_valid():
            # 新建数据
            nickname = form.cleaned_data.get('nickname')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            # 新建用户
            User.objects.create_user(username=nickname, password=password, email=email)
            # 注册成功记录 IP name 邮箱
            # logger.info('{} {} {}'.format())
            return json_response(errmsg='注册成功')
        else:
            # 将表单错误信息进行拼接
            err_msg_str = '/'.join([item[0] for item in form.errors.values()])

            return json_response(errno=Code.PARAMERR, errmsg=err_msg_str)

