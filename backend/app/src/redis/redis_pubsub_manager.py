import asyncio
# from redis.asyncio.client import PubSub, Redis
from app.src.redis.redis_connect import RedisConnect
from app.src.core.logging import logger
from aioredis.client import PubSub

class RedisPubSubManager:
    """
        Инициализация RedisPubSubManager.
    Args:
        redis_connection: RedisConnect
    """
    
    def __init__(self, redis_connection: RedisConnect):
        self.redis_connection = redis_connection
        logger.info("Created RedisPubSubManager")

    async def _publish(self, chanel_id: str, message: str) -> None:
        """
        Публикует сообщение в Redis channel.
        Args:
            chanel_id (str): Channel or chanel ID.
            message (str): Сообщение для публикации.
        """
        redis_connection = await self.redis_connection.get_redis_connection()
        await redis_connection.publish(channel=chanel_id, message=message)
        logger.info(f"RedisPubSubManager publish message {message} to chanel_id {chanel_id}")

    async def subscribe(self, chanel_id: str) -> PubSub:
        """
        Подписка на Redis channel.
        Args:
            chanel_id (str): Channel для подписки.
        Returns:
            aioredis.ChannelSubscribe: PubSub object для работы с подписками на канал.
        """
        
        redis_pubsub = await self.redis_connection.get_redis_pubsub()
        await redis_pubsub.subscribe(chanel_id)
            
        logger.info(f"RedisPubSubManager subscribe to chanel_id {chanel_id} redis_pubsub.channels {redis_pubsub.channels}")
        return redis_pubsub

    async def unsubscribe(self, chanel_id: str) -> None:
        """
        Описывает от Redis channel.

        Args:
            chanel_id (str): Channel unsubscribe from.
        """
        redis_pubsub = await self.redis_connection.get_redis_pubsub()
        await redis_pubsub.unsubscribe(chanel_id)
        logger.info(f"RedisPubSubManager unsubscribe from chanel_id {chanel_id} pubsub.channels {redis_pubsub.channels}")