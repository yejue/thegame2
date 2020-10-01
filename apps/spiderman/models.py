from django.db import models
from utils.validators import MediaUrlValidator

# Create your models here.


class SpiderData(models.Model):
    """
    爬虫数据表
    """
    false_data = models.CharField('扰乱数据', max_length=200)
    true_data = models.CharField('真实数据', max_length=50)
    data_index = models.CharField('数据索引', max_length=150)
    image_url = models.CharField("图片url", validators=[MediaUrlValidator], null=False, max_length=30)
    order = models.IntegerField("排序", default=0)

    class Meta:
        db_table = 'tb_data'                    # 指定迁移时的表名
        verbose_name = '爬虫数据表'
        verbose_name_plural = verbose_name


class SpiderEncrypt(models.Model):
    encrypt_data = models.CharField('加密数据', max_length=150)
    spider = models.ForeignKey(SpiderData, related_name='spider', on_delete=models.CASCADE)


class PassSave(models.Model):
    """
    牛逼的记录表 需要 userid作为外键， 一个初始化时间(后期不变化)
    """
    arrive_date = models.DateTimeField(auto_now_add=True)
    arrive_ip = models.CharField(max_length=20, null=True)

    user = models.ForeignKey('thecode.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_won'
        verbose_name = '通关记录表'
        verbose_name_plural = verbose_name
