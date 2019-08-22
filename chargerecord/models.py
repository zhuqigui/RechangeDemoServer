from django.db import models
from user.models import UserInfo


# Create your models here.

class OrderRecord(models.Model):
    """
    订单表
    """
    order_num = models.IntegerField(verbose_name='订单编号', unique=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    money = models.DecimalField(verbose_name='订单金额', max_digits=12, decimal_places=2)
    user = models.ForeignKey(to='user.UserInfo', on_delete=models.CASCADE, verbose_name='用户')
