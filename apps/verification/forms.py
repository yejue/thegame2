from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from thecode.models import User

# 邮箱校验
email_validator = RegexValidator('^.*?@.*?\.com|cn$', 1)


class CheckImageForm(forms.Form):
    """
    - 校验邮箱号码
    - 校验图形验证码
    - 校验是否在60s内有发送记录
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CheckImageForm, self).__init__(*args, **kwargs)

    email = forms.CharField(max_length=30, validators=[email_validator, ], error_messages={
        'max_length': '长度错误',
        'required': '邮箱是你的唯一认证，否则当你不是人',
    })
    image_code = forms.CharField(error_messages={
        'required': '图形验证码不能为空',
    })

    def clean(self):
        clean_data = super(CheckImageForm, self).clean()
        email = clean_data.get('email')
        image_code = clean_data.get('image_code')
        if email and image_code:
            # 校验图形验证码
            # 获取session中的验证进行比对
            image_codes = self.request.session.get('image_code')
            if not image_codes:
                raise forms.ValidationError('图形验证码失效')
            if image_code.upper() != image_codes.upper():
                raise forms.ValidationError('图形验证码输入错误')

            # 是否在60s 以内发送过邮件
            # 查询redis，存在则是60s内发送过
            redis_conn = get_redis_connection(alias='mailcode')
            if redis_conn.get('em_flag_{}'.format(email)):
                raise forms.ValidationError('验证码获取过于频繁')

            # 校验邮箱是否被注册
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('邮箱已被注册，请重新输入')

            return clean_data
