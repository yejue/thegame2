import random
import logging
import uuid
import logging

from django.http import HttpResponse
from django.views import View
from django_redis import get_redis_connection

from .constants import *
from .forms import CheckImageForm
from thecode.models import User
from utils.res_code import error_map, Code
from utils.sendMail import MailSender
from utils.genPic import gen_pure
from utils.genJsonResponse import json_response


logger = logging.getLogger('django')


def image_code_view(request):
    """
    图形验证码视图
    url: /veri/image_code
    :param request:
    :return:
    """
    # 1生成图形验证码
    text = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    print(text)
    img_code = gen_pure(109, 21, text)
    # 2保存验证码会话
    request.session['image_code'] = text
    request.session.set_expiry(300)
    # 3记录日志
    # logger.info('生成了图片{}'.format(text))
    # 4返回验证码图片
    return HttpResponse(img_code, content_type='img', charset='utf8')


class CheckEmailView(View):
    """
    url: /veri/email
    :return:
    """
    def post(self, request):
        email = request.POST.get('email')

        data = {
            'email': email,
            'count': User.objects.filter(email=email).count()
        }
        return json_response(data=data)


def check_nickname_view(request, nickname):
    """
    查询用户名是否存在
    url: /veri/check=(?P<nickname>.*?{5,20})
    :param request:
    :param nickname:
    :return:
    """
    data = {
            "nickname": nickname,                                       # 查询用户名
            "count": User.objects.filter(username=nickname).count()     # 查询用户数量
    }

    return json_response(data=data)


class SendMailView(View):
    """
    url: /veri/sendmail
    """
    def post(self, request):
        form = CheckImageForm(request.POST, request=request)

        if form.is_valid():
            email = request.POST.get('email')
            mailcode = uuid.uuid4().hex
            # 实例化邮件发送
            sender = MailSender([email], mailcode)
            sender.senderFunc()
            # 保存验证码 redis
            # 创建发送验证码记录的key
            em_flag_key = 'em_flag_{}'.format(email)
            em_text_key = 'em_text_{}'.format(email)
            redis_conn = get_redis_connection(alias='mailcode', )
            # 让管道通知redis
            pl = redis_conn.pipeline()

            try:
                # 设置生存时间与value
                pl.setex(em_flag_key, EM_CODE_INTERVAL, 1)
                pl.setex(em_text_key, EM_CODE_EXPIRES*60, mailcode)
                # 让管道通知 redis 执行
                pl.execute()
                return json_response(errmsg='验证码发送成功')
            except Exception as e:
                logger.error('redis 执行异常{}'.format(e))
                return json_response(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])
        else:
            # 将表单错误信息进行拼接
            err_msg_str = '/'.join([item[0] for item in form.errors.values()])
            return json_response(errno=Code.PARAMERR, errmsg=err_msg_str)

