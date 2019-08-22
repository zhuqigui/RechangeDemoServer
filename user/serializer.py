from datetime import datetime
import re

from django.contrib.auth.hashers import make_password, check_password
from django.db.utils import IntegrityError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.utils import jwt_payload_handler, jwt_decode_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings

from user.models import UserInfo, Wallet, FeedBack, WalletRecord
from utils.exception import TheBaseException
from xlr.settings import SECRET_KEY

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['phone', 'password']

    phone = serializers.CharField(error_messages={'required': '手机号必填'})
    password = serializers.CharField(error_messages={'required': '密码必填'})

    # def validated_email(self, value):
    #     if self.context._request.path != '/api/user/register/':
    #         return value
    #     pattern = '^[a-z0-9A-Z]+[- | a-z0-9A-Z . _]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$'
    #     if not re.match(pattern, value):
    #         raise TheBaseException(detail='邮箱格式不正确', code=1014)
    #     return value

    def validate_password(self, value):

        if len(value) < 5:
            raise TheBaseException(detail='密码长度必须大于6位', code=1012)
        if not value.isalnum():
            raise TheBaseException(detail='密码必须为数字字母组成', code=1013)

        return value

    def validate_phone(self, value):
        if self.context._request.path != '/api/user/register/':
            return value
        if len(value) != 11 or not value.isdigit() or UserInfo.objects.filter(phone=value).exists():
            raise TheBaseException(detail='号码已存在且必须为11位数字', code=1002)
        return value

    def user_register(self):
        """
        用户注册
        :return:
        """
        phone = self.validated_data.get('phone')
        pwd = self.validated_data.get('password')

        salt_pwd = make_password(pwd)

        wallet = Wallet.objects.create(money=100)
        user_obj = UserInfo.objects.create(phone=phone, password=salt_pwd, wallet=wallet)

        return user_obj

    def user_register2(self):
        phone = self.validated_data.get('phone')
        pwd = self.validated_data.get('password')
        email = self.validated_data.get('email')
        salt_pwd = make_password(pwd, salt=SECRET_KEY)
        if UserInfo.objects.filter(phone=phone).exists():
            raise TheBaseException(detail='该账号已注册', code=1016)

        wallet = Wallet.objects.create(money=100)
        user_obj = UserInfo.objects.create(phone=phone, password=salt_pwd, email=email, wallet=wallet)

        return user_obj

    # def user_register_backend(self, pwd, phone):
    #     """
    #     用户注册
    #     :return:
    #     """
    #     salt_pwd = make_password(pwd)
    #
    #     wallet = Wallet.objects.create(money=100)
    #     user_obj = UserInfo.objects.create(phone=phone, password=salt_pwd, wallet=wallet)
    #
    #     return user_obj

    def user_login(self):
        """
        用户登录
        :return:
        """
        phone = self.validated_data.get('phone')
        pwd = self.validated_data.get('password')
        user_obj = UserInfo.objects.filter(phone=phone).first()
        if not user_obj:
            raise TheBaseException(detail='用户不存在', code=1003)
        login_tag = check_password(pwd, user_obj.password)
        if not login_tag:
            raise TheBaseException(detail='用户或密码错误', code=1004)

        # 设置token

        payload = {
            'user_id': user_obj.pk,
            'phone': phone,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
        }

        token = jwt_encode_handler(payload)
        return user_obj, token


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletRecord
        fields = '__all__'

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj.pop('wallet')
        return obj
