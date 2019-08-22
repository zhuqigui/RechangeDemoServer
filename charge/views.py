import json
import random
import time
from functools import reduce
from threading import Timer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.transaction import atomic
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from dwebsocket.decorators import accept_websocket
from xlr.settings import FACILITY_SOCKET_DICT

from charge.models import Facility, Battery
from charge.serializer import FacilitySerializer, BatterySerializer
from chargerecord.models import OrderRecord
from user.models import Wallet
from utils.authentication import UserTokenAuthen
from utils.exception import TheBaseException


# 通知远端设备打开充电插槽
def open_the_slots(facility_num, slots_num):
    # 获取socket对象
    channel_name = FACILITY_SOCKET_DICT.get(facility_num)
    if not channel_name:
        raise TheBaseException(detail='该设备未连接', code=1008)
    # 推送消息
    channel_layer = get_channel_layer()
    print('发送websocket数据')
    queryset=Facility.objects.filter(facility_num=facility_num).first()
    serializer=FacilitySerializer(queryset,many=False)
    async_to_sync(channel_layer.send)(channel_name, {
        "type": "chat_message",
        "message": serializer.data,
        'hole_id': slots_num[-1],
    })
    # 修改订单状态


# 通知远端设备关闭插槽
def close_the_slots(facility_num, slots_num):
    # 本地修改插槽状态 ,对面需要做的事就是关闭or打开
    channel_name = FACILITY_SOCKET_DICT[facility_num]
    # 本地修改插槽状态
    channel_layer = get_channel_layer()


    fac_obj = Facility.objects.filter(facility_num=facility_num).first()
    setattr(fac_obj, slots_num, 0)
    fac_obj.save()
    serializer=FacilitySerializer(fac_obj,many=False)

    async_to_sync(channel_layer.send)(channel_name, {
        "type": "chat_message",
        "message": serializer.data,
        'hole_id': slots_num[-1],
    })


class FacilityView(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def list(self, request, *args, **kwargs):
        facility_id = self.request.query_params.get('facility_id')
        fac_obj = Facility.objects.filter(facility_num=facility_id).first()
        if not fac_obj:
            raise TheBaseException(detail='设备不存在', code=1012)
        serializer = FacilitySerializer(instance=fac_obj, many=False)

        return Response({'code': 200, 'data': serializer.data})

    @action(methods=['POST'], detail=False)
    def test(self, request):

        return Response({"code": 200, 'data': 'ok'})

    @action(methods=['POST'], detail=False, authentication_classes=[UserTokenAuthen])
    def order_submit(self, request, *args, **kwargs):
        user = request.user
        # 提交成功,添加订单记录 数据校验

        facility_num = request.data.get('facility_id')
        slots_id = request.data.get('hole_id')
        money = float(request.data.get('money'))
        facility_obj = Facility.objects.filter(facility_num=facility_num).first()
        if not facility_obj:
            raise TheBaseException(detail='设备不存在', code=1008)
        hole_status = getattr(facility_obj, 'slots{}'.format(slots_id))

        if hole_status != 0:
            raise TheBaseException(detail='设备繁忙，该插槽正在被使用', code=1009)
        # 判断余额是否足够
        wallet_obj = Wallet.objects.filter(userinfo=user).first()
        user_money = float(wallet_obj.money)
        if user_money - money < 0:
            raise TheBaseException(detail='余额不足请充值', code=1010)
        try:
            second = int(request.data.get('second'))
        except TypeError as e:
            raise TheBaseException(detail='second参数有误', code=1005)
        order_num = reduce(lambda x, y: str(x) + str(y), random.sample(range(0, 9), 9))
        # 修改用户金额
        data = {
            'msg': '订单提交成功',
        }

        with atomic():
            wallet_obj.money = user_money - money
            wallet_obj.save()
            setattr(facility_obj, 'slots{}'.format(slots_id), 1)
            facility_obj.save()
            OrderRecord.objects.create(order_num=order_num, money=money, user=user)
        # 打开插槽
        open_the_slots(facility_num, 'slots{}'.format(slots_id))
        # 异步关闭插槽
        Timer(second, close_the_slots, [facility_num, 'slots{}'.format(slots_id)]).start()
        return Response({'code': 200, 'data': data})


class BatteryView(APIView):

    def get(self, request, *args):
        all_battery_data = Battery.objects.all()
        serializer = BatterySerializer(instance=all_battery_data, many=True)
        return Response({'code': 200, 'data': serializer.data})
