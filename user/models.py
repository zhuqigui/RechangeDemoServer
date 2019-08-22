from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """
    用户信息表
    """
    phone = models.CharField(max_length=11, verbose_name='手机号码', unique=True)
    password = models.CharField(max_length=128, verbose_name='账号密码')
    city = models.CharField(max_length=64, verbose_name='城市', default='深圳')
    email = models.CharField(max_length=64, verbose_name='邮箱账号', default=None,null=True)
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, verbose_name='钱包')


class Wallet(models.Model):
    """
    钱包表
    """
    money = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='用户余额')


class WalletRecord(models.Model):
    """
    充值记录
    """
    record = models.DateTimeField(verbose_name='充值时间', auto_now_add=True)
    money = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='充值金额')
    wallet = models.ForeignKey(to='Wallet', on_delete=models.CASCADE)


class FeedBack(models.Model):
    """
    用户反馈表
    """
    content = models.TextField(verbose_name='反馈记录')
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='反馈')
