from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.


class User(AbstractUser):
    """
    AbstractUser原本已包含提示: username, first_name, last_name, email, is_active
    """
    class Meta:
        db_table = 'tb_user'                    # 指定迁移时的表名
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username, self.email

