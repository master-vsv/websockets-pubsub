import asyncio
from redis.asyncio.client import PubSub, Redis
from app.src.redis.redis_connect import RedisConnect 

class RedisPubSubManager:
    """
        Initializes the RedisPubSubManager.

    Args:
        redis_connection: RedisConnect
    """
    
    def __init__(self, redis_connection: RedisConnect):
        self.redis_connection = redis_connection

    async def _publish(self, chanel_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            chanel_id (str): Channel or chanel ID.
            message (str): Message to be published.
        """
        redis_connection = await self.redis_connection.get_redis_connection()
        await redis_connection.publish(channel=chanel_id, message=message)

    async def subscribe(self, chanel_id: str) -> PubSub:
        """
        Subscribes to a Redis channel.

        Args:
            chanel_id (str): Channel or chanel ID to subscribe to.

        Returns:
            aioredis.ChannelSubscribe: PubSub object for the subscribed channel.
        """
        redis_pubsub = await self.redis_connection.get_redis_pubsub()
        self.pubsub: PubSub = await redis_pubsub.subscribe(chanel_id)
        return self.pubsub

    async def unsubscribe(self, chanel_id: str) -> None:
        """
        Unsubscribes from a Redis channel.

        Args:
            chanel_id (str): Channel or chanel ID to unsubscribe from.
        """
        redis_pubsub = await self.redis_connection.get_redis_pubsub()
        await redis_pubsub.unsubscribe(chanel_id)