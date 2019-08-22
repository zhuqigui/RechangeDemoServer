from __future__ import absolute_import
import json
import random
from celery import shared_task
from xlr.celery import app
from django.core.cache import cache
import requests
from django.core.mail import send_mail
from xlr import settings


@app.task()
def send_vcode(phone):
    url = settings.YZX_URL
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8',
    }
    data = {
        'token': settings.YZX_TOKEN,
        'sid': settings.YZX_SID,
        'appid': settings.YZX_APPID,
        'templateid': settings.YZX_TEMPLATEID,
        'mobile': phone,
        'param': random.randint(100000, 999999),
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    code = response.json()['code']
    if code == "000000":
        print(data['mobile'], type(data['mobile']))
        cache.set(data['mobile'], data['param'])
        return 'SUCCESS'
    return 'FAIL'


@app.task
def send_email_code(email_num, phone):
    msg = '小绿人小程序欢迎您的使用'
    content = '用户密码修改'
    code = random.randint(000000, 999999)
    html_msg = '<h1 style=color:red;>验证码是：{} 请30分钟内激活</h1> '.format(code)
    send_mail(msg, content, settings.EMAIL_FROM, [email_num], html_message=html_msg)
    cache.set(phone, code, 60 * 30)
    return 'ok'
