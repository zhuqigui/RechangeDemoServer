from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_jwt.utils import jwt_payload_handler, jwt_decode_handler, jwt_encode_handler
from rest_framework.pagination import PageNumberPagination

from user.models import UserInfo, Wallet, WalletRecord
from user.serializer import UserSerializer, WalletSerializer, WalletRecordSerializer
from user.tasks import send_vcode, send_email_code
from utils.authentication import UserTokenAuthen
from utils.exception import TheBaseException
from utils.pagination import WalletRecordPagination
from xlr.settings import FACILITY_SOCKET_DICT, SECRET_KEY


class UserView(GenericViewSet, ListModelMixin, CreateModelMixin):
    """
    用户视图
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [UserTokenAuthen, ]

    def list(self, request, *args, **kwargs):
        user = request.user

        wallet = WalletSerializer(instance=user.wallet, many=False).data.get('money')
        data = {

            "id": user.id,
            "phone": user.phone,
            "city": user.city,
            "wallet": wallet,
        }
        return Response({'code': 200, 'data': data})

    @action(methods=['POST'], detail=False, authentication_classes=[])
    def login(self, request, *args):
        """
        用户登录
        """
        serializer = UserSerializer(data=self.request.data, context=request)
        serializer.is_valid(raise_exception=True)
        # 用户登录之后的token
        user_obj, token = serializer.user_login()

        data = {
            'phone': user_obj.phone,
            'token': token,
            'city': user_obj.city,
            'msg': '登录成功'

        }

        return Response({'code': 200, 'data': data})

    @action(methods=['POST'], detail=False, authentication_classes=[])
    def register(self, request, *args):
        """
        用户注册
        """
        serializer = UserSerializer(data=self.request.data, context=request)
        serializer.is_valid(raise_exception=True)
        # 注册功能
        obj = serializer.user_register()

        data = {
            'phone': obj.phone,
            'msg': '注册成功',
        }
        return Response({'code': 200, 'data': data})

    @action(methods=['POST'], detail=False, authentication_classes=[])
    def register2(self, request, *args):
        serializer = UserSerializer(data=self.request.data, context=request)
        serializer.is_valid(raise_exception=True)

        obj = serializer.user_register2()

        data = {
            'phone': obj.phone,
            'email': obj.email,
            'msg': '注册成功',
        }
        return Response({'code': 200, 'data': data})

    # @action(methods=['POST'], detail=False, authentication_classes=[])
    # def register_backend(self, request, *args):
    #     """
    #     用户注册,增加验证码功能
    #     """
    #     serializer = UserSerializer(data=self.request.data, context=request)
    #     serializer.is_valid(raise_exception=True)
    #     phone = serializer.validated_data.get('phone')
    #     pwd = serializer.validated_data.get('password')
    #     vcode = self.request.data.get('vcode')
    #     old_vcode = cache.get(phone)
    #     if vcode != old_vcode:
    #         raise TheBaseException(detail='验证码有误', code=1011)
    #
    #     serializer.user_register_backend(pwd, phone)
    #     data = {
    #         'phone': phone,
    #         'msg': '注册成功',
    #     }
    #     return Response({'code': 200, 'data': data})

    @action(methods=['GET'], detail=False, authentication_classes=[])
    def verify_code(self, request):
        phone = self.request.query_params.get('phone')

        send_vcode.delay(phone)
        data = {
            'msg': '验证码发送成功'
        }
        return Response({'code': 200, 'data': data})

    @action(methods=['GET'], detail=False)
    def wallet(self, request, *args):
        # TODO
        print(FACILITY_SOCKET_DICT)
        user = request.user
        wallet = WalletSerializer(instance=user.wallet, many=False).data.get('money')
        data = {
            'money': wallet,
            'msg': '获取钱包信息成功',

        }

        return Response({'code': 200, 'data': data})

    # 钱包记录接口
    @action(methods=['GET'], detail=False)
    def wallet_detail(self, request, *args):
        user = request.user
        queryset = WalletRecord.objects.filter(wallet=user.wallet)
        page_obj = WalletRecordPagination()
        page_list = page_obj.paginate_queryset(queryset, request, self)

        serializer = WalletRecordSerializer(instance=page_list, many=True)
        data = {
            'record': serializer.data
        }
        return Response({'code': 200, 'data': data})

    @action(methods=['POST'], detail=False)
    def change_password(self, request, *args):
        oldpwd = request.data.get('oldpwd')
        newpwd = request.data.get('newpwd')

        if not all([oldpwd, newpwd]):
            raise TheBaseException(detail='数据校验格式失败', code=1007)
        user_obj = request.user
        tag = check_password(oldpwd, user_obj.password)
        if not tag:
            raise TheBaseException(detail='密码不一致', code=1006)
        # 修改密码
        user_obj.password = make_password(newpwd)
        user_obj.save()

        data = {
            'msg': '修改密码成功',

        }
        return Response({'code': 200, 'data': data})

    @action(methods=['POST'], detail=False)
    def change_password2(self, request, *args):
        vcode = self.request.data.get('vcode')
        phone = self.request.data.get('phone')
        newpwd = self.request.data.get('newpwd')
        user = request.user
        re_vcode = cache.get(phone)
        # 判断验证码
        if str(vcode) != str(re_vcode):

            raise TheBaseException(detail='验证码有误', code=1011)
        # 密码校验
        if user.password == make_password(newpwd, SECRET_KEY):
            raise TheBaseException(detail='不能与近期使用过的密码相似', code=1015)
        if len(newpwd) < 5:
            raise TheBaseException(detail='密码长度必须大于等于6位', code=1012)
        if not newpwd.isalnum():
            raise TheBaseException(detail='密码必须由字母或数字组成', code=1006)
        # 修改密码
        user.password = make_password(newpwd, SECRET_KEY)
        user.save()
        data = {
            'msg': '修改密码成功',

        }
        return Response({'code': 200, 'data': data})

    @action(methods=['POST'], detail=False, authentication_classes=[])
    def delete_user(self, request, *args):
        phone = request.data.get('phone')
        UserInfo.objects.filter(phone=phone).delete()
        data = {
            'msg': '删除成功'
        }
        return Response({'code': 200, 'data': data})


def send_email(request):
    # 异步执行任务
    email = request.GET.get('email')
    phone = request.GET.get('phone')

    send_email_code.delay(email, phone)

    data = {
        'msg': '发送成功',
    }
    return JsonResponse({'code': 200, 'data': data})
