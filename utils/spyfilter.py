import re


class ReqFilter:
    ua_not_allow = [
        'python', 'curl', 'java', 'w3m', 'c++'
    ]
    accept_list = [
        'application/json'
    ]
    accept_language = [
        'zh-CN,zh;q=0.9'
    ]
    # 一般页面 meta
    get_list = [
        'HTTP_ACCEPT_LANGUAGE', 'HTTP_UPGRADE_INSECURE_REQUESTS'
    ]

    # 接口处 meta
    get_list_api = [
        'HTTP_ACCEPT_LANGUAGE'
    ]
    # api referer
    api_referer = '.*?/spider/spiderdata/.*?'

    @staticmethod
    def meta_filter(request, filters: list):
        for f in filters:
            if not request.META.get(f):
                return True
        return False

    @staticmethod
    def ua_filter(request, filters: list):
        ua = request.headers.get('User-Agent')
        if not ua:
            return True
        for f in filters:
            if f in ua:
                return True
        return False

    @staticmethod
    def accept_filter(request, filters: list):
        accept = request.headers.get('Accept')
        if not accept:
            return True
        for f in filters:
            if f not in accept:
                return True
        return False

    @staticmethod
    def lang_filter(request, filters: list):
        accept_lang = request.headers.get('Accept-Language')
        if not accept_lang:
            return True
        for f in filters:
            if f not in accept_lang:
                return True
        return False

    def referer_filter(self, request, referer: str):
        ref = request.headers.get('Referer')
        re_ref = re.compile(self.api_referer)
        if not ref:
            return True
        if not re_ref.findall(ref):
            return True
        return False

    def combine_api_filter(self, request):
        # ua 检测，meta检测，accept检测 json, referer
        combine_list = [
            self.meta_filter(request, self.get_list_api), self.ua_filter(request, self.ua_not_allow),
            self.accept_filter(request, self.accept_list), self.referer_filter(request, self.api_referer)
        ]
        for one in combine_list:
            if one:
                return True

    def combine_general(self, request):
        # ua 检测， meta检测
        combine_list = [
            self.meta_filter(request, self.get_list), self.ua_filter(request, self.ua_not_allow),
        ]
        for one in combine_list:
            if one:
                return True
