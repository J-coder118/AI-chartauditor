import json
from channels.generic.websocket import AsyncConsumer


class ProgressBarConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print("websocket connected")
        # print('channel layers:::::', self.channel_layer)
        # print('channel layers:::::', self.channel_name)
        user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = str(user_id)
        # print('user_id', type(self.group_name))
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        # print(f'message: {event["text"]}')
        # print('message', type(event["text"]))
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'message': event['text']
        })

    async def chat_message(self, event):
        # print('event:::', event)
        # print('actual data:::', event['message'])
        # print('actual data type:::', type(event['message']))
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(event["message"])
        })

    async def websocket_disconnect(self, event):
        # print('websocket disconnected')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)