import asyncio

import json
from fastapi import WebSocket
from app.src.redis.redis_pubsub_manager import RedisPubSubManager
from app.src.redis.redis_connect import RedisConnect
from app.src.core.settings import settings
from redis.asyncio.client import PubSub, Redis

class WebSocketManager:

    def __init__(self, redis_connection: RedisConnect):
        """
        Инициализация WebSocketManager.

        Attributes:
            chanels (dict): Словарь хранит канал и его WebSockets.
            pubsub_client (RedisPubSubManager): Экземпляр RedisPubSubManager class для работы с pub-sub.
        """
        self.chanels: dict[str,list[WebSocket]] = {}
        self.pubsub_client = RedisPubSubManager(redis_connection)

    async def add_websocket_to_chanel(self, chanel_id: str, websocket: WebSocket) -> None:
        """ Добавляет WebSocket в канал.
        Args:
            chanel_id (str): channel name.
            websocket (WebSocket): WebSocket connection object.
        """
        await websocket.accept()

        if chanel_id not in self.chanels:
            if len(self.chanels) == 0:
                self.chanels[chanel_id] = [websocket]
            else:
                self.chanels[chanel_id].append(websocket)
      
        pubsub_subscriber: PubSub = await self.pubsub_client.subscribe(chanel_id)
        if pubsub_subscriber is not None:
            asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))
        print(self.chanels)
            
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """ Отправляет персональное сообщение в websocket """
        await websocket.send_text(message)
        print("Sent a personal msg to , ", websocket)

    async def broadcast_to_chanel(self, chanel_id: str, message: str) -> None:
        """
        Публикует сообщение во все WebSockets канала.

        Args:
            chanel_id (str): chanel ID or channel name.
            message (str): Message to be broadcasted.
        """
        await self.pubsub_client._publish(chanel_id, message)

    async def remove_user_from_chanel(self, chanel_id: str, websocket: WebSocket) -> None:
        """ Удаляет WebSocket из канала.
        Args:
            chanel_id (str): chanel name.
            websocket (WebSocket): WebSocket connection object.
        """
        self.chanels[chanel_id].remove(websocket)

        if len(self.chanels[chanel_id]) == 0:
            del self.chanels[chanel_id]
            await self.pubsub_client.unsubscribe(chanel_id)

    async def _pubsub_data_reader(self, pubsub_subscriber: PubSub):
        """ Читает и публикует в WebSockets сообщения полученные от Redis PubSub.
        Args:
            pubsub_subscriber (aioredis.ChannelSubscribe): PubSub object for the subscribed channel.
        """
        while True:
            # if pubsub_subscriber is not None:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True, timeout=0.1)
            print(message)

            if message is not None:
                chanel_id = message['channel'].decode('utf-8')
                all_sockets = self.chanels[chanel_id]
                for socket in all_sockets:
                    data = message['data'].decode('utf-8')
                    await socket.send_text(data)
            # else: print("pubsub_subscriber - пуст")
