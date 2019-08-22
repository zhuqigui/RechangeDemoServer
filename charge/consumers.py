import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from xlr.settings import FACILITY_SOCKET_DICT


class FacilityConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user_id = self.scope['query_string'].decode().partition('=')[-1]
        FACILITY_SOCKET_DICT[user_id] = self.channel_name
        print(FACILITY_SOCKET_DICT)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group

        print('连接断开', close_code)

        # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        # await self.channel_layer.send(self.channel_name, {
        #     "type": "chat_message",
        #     "message": '服务器发来的消息',
        #     'hole_id': 1,
        # })

    async def chat_message(self, event):
        message = event['message']
        hole_id = event['hole_id']

        # 数据序列化
        await self.send(text_data=json.dumps({
            'message': message,
            'hole_id': hole_id

        }))
