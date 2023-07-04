from django.urls import re_path, path
from manager import consumers


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()),
    re_path(r"ws/chat/orders/(?P<order_id>\w+)/$", consumers.OrderChatRoom.as_asgi()),
]