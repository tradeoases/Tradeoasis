from operator import le
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json
from manager import models as ManagerModels
from auth_app import models as AuthModels
from django.db.models import Q
from django.conf import settings
import os

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # name of the chatroom
        self.room_name = self.scope['url_route']['kwargs']['room_name']

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

        file_path = os.path.join(settings.CHATROOMFILES_DIR, f"{self.scope['url_route']['kwargs']['room_name']}.json")
        with open(file_path, "r") as file:
            current_data = json.load(file)
            for i in range(len(current_data)):
                await self.send(text_data=json.dumps(current_data[i]))


    async def disconnect(self, code):
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )
        await super().disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        roomname = self.scope['url_route']['kwargs']['room_name']
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        username = text_data_json['username']
             
        await database_sync_to_async(self.storechatroom)(message, user, username)

        await self.write_message_to_file(roomname, user, username, message)

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

    def storechatroom(self, message, account_type, username):
        roomname = self.scope['url_route']['kwargs']['room_name']
        user = AuthModels.User.objects.filter(username=username).first()
        if user:
            if not ManagerModels.Chatroom.objects.filter(roomname=roomname).exists():
                # create database record
                ManagerModels.Chatroom.objects.create(
                    roomname = roomname,
                    user = user,
                )
            elif ManagerModels.Chatroom.objects.filter(Q(roomname=roomname), Q(is_handled=False)).exists() and account_type == "Support":
                # set support handling a chat
                chatroom = ManagerModels.Chatroom.objects.filter(Q(roomname=roomname), Q(is_handled=False)).first()
                user_profile = AuthModels.SupportProfile.objects.filter(user=user).first()
                chatroom.support = user_profile
                chatroom.is_handled = True
                chatroom.save()
                user_profile.increase_responses_count()

    @sync_to_async
    def write_message_to_file(self, roomname, user, username, message):
        file_path = os.path.join(settings.CHATROOMFILES_DIR, f"{roomname}.json")
        with open(file_path, "r") as file:
            current_data = json.load(file)
            current_data.append({
                "user": user,
                "username" : username,
                "message" : message,
            })

        with open(file_path, 'w') as file:
            json.dump(current_data, file)