from django.urls import path
from .consumers import UpgradeChatRequestConsumer

websocket_urlpatterns = [
    path('ws/request/<room_name>/', UpgradeChatRequestConsumer.as_asgi())
]