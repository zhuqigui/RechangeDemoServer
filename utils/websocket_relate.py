import json


def test_send_msg(obj):
    obj.send(json.dumps('测试数据').encode())
