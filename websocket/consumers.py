import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'] == None:
            raise Exception('User not found')
        else:
            self.user = self.scope['user']
        self.project_pk = self.scope['url_route']['kwargs']['project_pk']
        self.room_group_name = 'chat_project%s' % self.project_pk

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        def message_serializer(project_pk, user_id, json_data):
            text_data_json = json.loads(json_data)
            serializer = MessageSerializer(data={
                'content': text_data_json['content'],
            })

            if serializer.is_valid():
                serializer.save(project_id=project_pk, owner_id=user_id)
            return serializer.data

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': await sync_to_async(message_serializer)(self.project_pk, self.user.id, text_data)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        if 'project' in message:
            del message['project']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class ActivityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'] == None:
            raise Exception
        else:
            self.user = self.scope['user']
        self.room_group_name = 'activity_%s' % self.user.id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
