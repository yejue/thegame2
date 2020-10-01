def get_ip(request):
    """
    返回访问对象的 ip
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0] or 0         # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR', None)            # 这里获得代理ip
    return ip
