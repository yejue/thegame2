import re
from urllib.parse import quote
from django import forms
from django.http import HttpResponse
from django.contrib.auth import login
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from .models import User
from .constants import *
from verification.forms import email_validator


# 昵称限制 5~20个字母或数字
nickname_validators = RegexValidator('^\w{2,20}$', 1)


class RegisterForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    nickname = forms.CharField(label='昵称', max_length=MAX_USERNAME_LENGTH, min_length=MIN_USERNAME_LENGTH,
                               validators=[nickname_validators],
                               error_messages={
                                   'max_length': '昵称长度错误',
                                   'min_length': '昵称长度错误',
                                   'validators': '昵称格式为2~20任意字符',
                                   'required': '昵称不能为空',
                               })
    password = forms.CharField(label='密码', max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH,
                               error_messages={
                                   'max_length': '密码长度错误',
                                   'min_length': '密码长度错误',
                                   'required': '密码不能为空',
                               })
    password_repeat = forms.CharField(label='重复密码', max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH,
                                      error_messages={
                                          'max_length': '密码最大长度为{}'.format(MAX_PASSWORD_LENGTH),
                                          'min_length': '密码长度至少为{}'.format(MIN_PASSWORD_LENGTH),
                                          'required': '密码不能为空',
                                      })

    email = forms.CharField(label='邮箱',
                            max_length=30, validators=[email_validator, ],
                            error_messages={
                                 'max_length': '邮箱长度错误',
                                 'min_length': '邮箱长度错误',
                                 'required': '邮箱不能为空',
                             })
    mailcode = forms.CharField(label='邮箱验证码', error_messages={'required': '验证码不能为空'})

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(username=nickname).exists():
            raise forms.ValidationError('昵称已存在')
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean(self):
        cleaned_data = super().clean()
        nickname = cleaned_data.get('nickname')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        mailcode = cleaned_data.get('mailcode')

        # 校验两次输入的密码是否一致
        if password != password_repeat:
            raise forms.ValidationError('两次输入的密码不一致')

        # 校验验证码是否正确
        # 连接redis
        redis_conn = get_redis_connection(alias='mailcode')
        real_em_code = redis_conn.get('em_text_{}'.format(email))
        if not real_em_code and mailcode != real_em_code:
            raise forms.ValidationError('邮箱验证码错误')

        return cleaned_data


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LoginForm, self).__init__(*args, **kwargs)

    nickname = forms.CharField(error_messages={'required': '请输入正确的昵称或密码'})

    password = forms.CharField(label='密码', max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH,
                               error_messages={
                                   'max_length': '密码长度错误',
                                   'min_length': '密码长度错误',
                                   'required': '密码不能为空',
                               })
    rand = forms.CharField(label="随机")

    def clean_account(self):
        nickname = self.cleaned_data.get('nickname')
        if not re.match('^\w{2,20}$', nickname):
            raise forms.ValidationError('昵称或密码输入错误')
        return nickname

    def clean(self):
        cleaned_data = super().clean()
        rand = cleaned_data.get('rand')
        if not rand:
            raise forms.ValidationError("爬虫警告")
        nickname = cleaned_data.get('nickname')
        password = cleaned_data.get('password')

        # 找到用户，校验密码
        user_querySet = User.objects.filter(username=nickname)
        if user_querySet:
            user = user_querySet.first()
            if user.check_password(password):
                # 免登陆
                # self.request.session.set_expiry(REMENBER_LOGIN_TIME * 24 * 60 * 60)
                self.request.session.set_expiry(DEFAULT_LOGIN_TIME * 60)
                print(dir(self.request))
                print(self.request.COOKIES)
                login(self.request, user)
            else:
                raise forms.ValidationError('昵称或密码输入错误')
        else:
            raise forms.ValidationError('昵称或密码输入错误')

        return cleaned_data
