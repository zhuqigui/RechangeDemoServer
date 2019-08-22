from django.db import models


# Create your models here.

class Battery(models.Model):
    """
    电池表
    """
    name = models.CharField(max_length=32, verbose_name='电池类型名称', unique=True)
    price_policy = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='价格策略')


class Facility(models.Model):
    """
    设备表
    """
    USE_STATUS = (
        (0, '空闲'),
        (1, '使用中'),
    )
    facility_num = models.IntegerField(verbose_name='设备编号', unique=True)
    slots1 = models.SmallIntegerField(choices=USE_STATUS, verbose_name='一号插槽', default=0)
    slots2 = models.SmallIntegerField(choices=USE_STATUS, verbose_name='二号插槽', default=0)
    slots3 = models.SmallIntegerField(choices=USE_STATUS, verbose_name='三号插槽', default=0)
    slots4 = models.SmallIntegerField(choices=USE_STATUS, verbose_name='四号插槽', default=0)
    slots5 = models.SmallIntegerField(choices=USE_STATUS, verbose_name='五号插槽', default=0)
    slots6 = models.SmallIntegerField(choices=USE_STATUS, verbose_name='六号插槽', default=0)
    city = models.CharField(verbose_name='城市', max_length=16, default='深圳')
    addr = models.CharField(verbose_name='地址', max_length=255,null=True)
