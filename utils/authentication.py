import time
import datetime

import jwt
from rest_framework import exceptions
from rest_framework_jwt.utils import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.translation import ugettext as _

from user.models import UserInfo
from utils.exception import TheBaseException


class UserTokenAuthen(BaseAuthentication):
    """
    用户认证 使用jwt
    """

    def authenticate(self, request):
        token = request._request.META.get('HTTP_AUTHORIZATION')
        phone = str(request.query_params.get('phone', '')) or str(request.data.get('phone', ''))
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise TheBaseException(detail=msg,code=1005)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise TheBaseException(detail=msg,code=1005)
        except jwt.InvalidTokenError:
            raise TheBaseException(detail='token验证失败',code=1005)

        user = UserInfo.objects.filter(phone=phone).first()

        if user is None or phone != payload['phone']:
            raise TheBaseException(detail='手机号必填 or Error decoding signature.', code=1005)
        return user, token
