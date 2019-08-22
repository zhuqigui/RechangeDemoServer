from functools import reduce
import json

from django.test import TestCase
from rest_framework.decorators import api_view
# Create your tests here.
# import pymysql
#
# db = pymysql.Connection(host='127.0.0.1', user='root', password="root",
#                         database='xlr', port=3306, )
# cursor=db.cursor()
#
# print(cursor.execute())
#
#
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xlr.settings")
django.setup()
#
# from django.contrib.auth.hashers import make_password, check_password
#
# from user.models import UserInfo
#
# all_user=UserInfo.objects.filter(phone='asd')
# print(all_user.first())


# import random
# from django.core.cache import cache
# import requests
# from xlr import settings
#
# def send_vcode():
#     url = settings.YZX_URL
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json;charset=utf-8',
#     }
#     data = {
#         'token': settings.YZX_TOKEN,
#         'sid': settings.YZX_SID,
#         'appid': settings.YZX_APPID,
#         'templateid': settings.YZX_TEMPLATEID,
#         'mobile': '18046665636',
#         'param': random.randint(100000, 999999),
#     }
#
#     print(url)
#     response = requests.post(url=url, headers=headers, data=json.dumps(data))
#
#     # data=json.loads(response.json())
#     print(type(response.json()['code']))
#     print(response.json())
#     # if data['code']!= '000000':
#     #     print("失败")
#     # else:
#     #     print("success")
#
#
#
# send_vcode()
