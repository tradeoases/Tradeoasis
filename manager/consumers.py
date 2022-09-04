from email import message
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # name of the chatroom
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # create database record

        # group users in a specific chatroom
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

        await self.channel_layer.group_send (
            self.room_group_name,
            {
                "type": "initial_message",
                "message": "Hello. What can i help you with?",
                "user": "support",
            }
        )

    async def initial_message(self, event):
        message = event['message']
        user = "Support"
    
        await self.send(text_data=json.dumps({
            "message" : message,
            "user" : user
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        username = text_data_json['username']

        await self.channel_layer.group_send (
            self.room_group_name,
            {
                "type": "chatroom_message",
                "message": message,
                "username" : username,
                "user": user,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        user = event['user']
        username = event['username']
    
        await self.send(text_data=json.dumps({
            "message" : message,
            "username" : username,
            "user" : user
        }))