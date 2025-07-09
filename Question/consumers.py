# Question/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # لو احتجنا مستقبل من العميل، نستخدم هاد
        pass

    async def send_notification(self, event):
        # إرسال إشعار مع تفاصيل إضافية (نص السؤال أو الجواب)
        await self.send(text_data=json.dumps({
            'message': event.get('message', ''),
            'text': event.get('text', ''),
            'sender': event.get('sender', ''),
            'timestamp': event.get('timestamp', ''),
        }))
