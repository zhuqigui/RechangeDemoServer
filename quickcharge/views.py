from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from django.db.transaction import atomic

from user.models import Wallet, UserInfo, WalletRecord
from user.serializer import WalletSerializer
from utils.authentication import UserTokenAuthen
from utils.exception import TheBaseException


class QuickChargeMoney(GenericViewSet, CreateModelMixin):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    authentication_classes = [UserTokenAuthen, ]

    @action(methods=['POST'], detail=False)
    def pushmoney(self, request, *args, **kwargs):
        user_obj = request.user
        money = str(request.data.get('money'))
        if not money.isdigit():
            raise TheBaseException(detail='数据校验失败', code=1007)
        # 1.修改用户余额
        # 2.添加充值记录
        with atomic():
            wallet_obj = Wallet.objects.filter(userinfo=user_obj).first()
            calc_money = float(wallet_obj.money) + float(money)
            wallet_obj.money = calc_money
            wallet_obj.save()
            WalletRecord.objects.create(money=money, wallet=wallet_obj)

        data = {
            'msg': '充值成功',
            'money': wallet_obj.money,
        }
        return Response({'code': 200, 'data': data})
