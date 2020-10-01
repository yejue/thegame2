import logging
import random
import time
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_redis import get_redis_connection
from django.db.models import F

from utils.genData import InsertData
from utils.genJsonResponse import json_response
from utils.getUserMeta import get_ip
from utils.spyfilter import ReqFilter
from utils.res_code import *
from .constants import *
from .models import SpiderData, PassSave, SpiderEncrypt
# Create your views here.

logger = logging.getLogger('thegame')
logger2 = logging.getLogger('django')


@method_decorator(login_required, name='get')
class SpiderDataView(View):
    """
    url: spider/spiderdata
    返回数据页
    """

    def get(self, request):
        req_filter = ReqFilter()
        if req_filter.combine_general(request):
            return HttpResponse(PIKAQIU+BLOG_URL, status=418)
        logger2.info('有人访问 {}'.format(get_ip(request)))
        return render(request, 'spiderman/spiderdata.html')


@method_decorator(login_required, name='get')
class SpiderDataListView(View):
    """
    url: spider/spiderdata/data
    每一个请求给出5页
    """
    def get(self, request):
        # 访问redis，查看是否存在，存在返回皮卡丘
        ip = get_ip(request)
        redis_conn = get_redis_connection(alias='request_interval')
        if redis_conn.get('req_flag_{}'.format(ip)):
            return HttpResponse(MIGUAN, status=418)
        # 对请求进行鉴别
        req_filter = ReqFilter()
        if req_filter.combine_api_filter(request):
            return HttpResponse(BLOG_URL+PIKAQIU+MIGUAN, status=418)
        try:
            page = int(request.GET.get('page') or 1)
        except ValueError:
            return HttpResponse(PIKAQIU, status=418)
        # 获取查询集
        spider_data = SpiderData.objects.values(
            'false_data',  'data_index', 'image_url', 'order',
        ).annotate(encrypt_data=F('spider__encrypt_data')).order_by('id')

        # 分页
        paginator = Paginator(spider_data, 5)
        # 当前页数据
        spider_info = paginator.get_page(page)

        # 送入redis
        req_flag_key = 'req_flag_{}'.format(ip)
        # 让管道通知redis
        pl = redis_conn.pipeline()

        try:
            # 设置生存时间与value
            pl.setex(req_flag_key, REQUEST_INTERVAL, 1)
            # 让管道通知 redis 执行
            pl.execute()
        except Exception as e:
            logger2.error('redis 执行异常{}'.format(e))
            return json_response(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])

        data = {
            'total_pages': paginator.num_pages,
            'spider': list(spider_info)
        }
        return json_response(data=data)


@method_decorator(login_required, name='post')
class AnswerView(View):
    """
    答案页面
    """
    def get(self, request):
        pass_user = PassSave.objects.order_by('arrive_date').all()
        return render(request, 'spiderman/code.html', context={
            'ps': pass_user
        })

    def post(self, request):
        answer = request.POST.get('answer')
        if answer == '一别三季庆国庆月又新年':
            # 记录日志
            ip = get_ip(request)
            logger.info("{}, {}完成了挑战".format(request.user.username, get_ip(request)))
            # 记录到通关表
            if not PassSave.objects.filter(user=request.user).exists():
                ps = PassSave(user=request.user, arrive_ip=ip)
                ps.save()
            else:
                return HttpResponse('{} {} 已完成通关，勿重复提交'.format(request.user.username, ip))
            return HttpResponse("{} 恭喜你，攻略完毕，已计入排行".format(time.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            return HttpResponse('不正确')


class AddDataToMysql(View):
    """
    url : spider/add
    写入数据库 部署时取消
    """
    def get(self, request):
        import random
        temp_list = []
        yibie = '₸3Ⱳq国q月又新年'
        chengyu = '左顾右盼、东张西望、望眼bai欲穿、极目远望、' \
                  '望洋兴叹、刮目相看、另眼du相看、走马观花、zhi瞠目而视、' \
                  '高步阔视、虎视眈眈、目不斜视、目不忍视、察颜观色、冷眼旁观、' \
                  '束手旁观、坐井观天兴高采烈、喜出望外、喜形于色、喜上眉梢、喜不自胜、' \
                  '喜不自禁、喜眉笑眼、喜气洋洋、喜笑颜开、笑逐颜开、心旷神怡、心满意足、心情舒畅' \
                  '、心醉神迷、心花怒放、乐乐陶陶、其乐融融、乐以忘忧、乐不可支、欣喜若狂'

        for i in range(1, 11):
            temp_dict = {'data': list(yibie)[i - 1], 'td': True, 'index': str(i)}
            temp_list.append(temp_dict)

        for i in range(1000):
            temp_dict = {'data': random.choice(chengyu.split('、')), 'index': '假的'}
            temp_list.append(temp_dict)

        random.shuffle(temp_list)

        if not temp_list[5].get('td'):
            temp_list[5] = {'data': 'A', 'td': 'True', 'index': '0'}
        else:
            temp_list.append({'data': 'A', 'td': 'True', 'index': '0'})
        count = 0
        for item in temp_list:
            shit_data = InsertData.shit_data()
            spi = SpiderData.objects.create(
                false_data=shit_data, true_data=item['data'], data_index=item['index'], order=count,
                image_url='{}.jpg'.format(random.randint(7, 8))
            )
            spi.save()
            spi.spider.create(encrypt_data=self.hanshu(spi.true_data))
            count += 1
        return HttpResponse('添加完成')

    @staticmethod
    def hanshu(s: str):
        return ''.join([chr(i2) for i2 in [ord(i)+2 for i in s]])

