import asyncio
from redis.asyncio.client import PubSub, Redis
from src.redis.redis_connect import RedisConnect 

class RedisPubSubManager:
    """
        Initializes the RedisPubSubManager.

    Args:
        host (str): Redis server host.
        port (int): Redis server port.
    """
    
    def __init__(self, redis_connection: RedisConnect):
        self.redis_connection = redis_connection

    # def __init__(self, host='localhost', port=6379):
    #     self.redis_host = host
    #     self.redis_port = port
    #     self.pubsub: aioredis.Redis | None = None
        
    # async def _get_redis_connection(self) -> aioredis.Redis:
    #     """
    #     Establishes a connection to Redis.

    #     Returns:
    #         aioredis.Redis: Redis connection object.
    #     """
    #     return aioredis.Redis(host=self.redis_host,
    #                           port=self.redis_port,
    #                           auto_close_connection_pool=False)

    # async def connect(self) -> None:
    #     """
    #     Connects to the Redis server and initializes the pubsub client.
    #     """
    #     self.redis_connection = await self._get_redis_connection()
    #     self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, chanel_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.

        Args:
            chanel_id (str): Channel or chanel ID.
            message (str): Message to be published.
        """
        redis_connection = await self.redis_connection.get_redis_connection()
        await redis_connection.publish(channel=chanel_id, message=message)

    async def subscribe(self, chanel_id: str) -> Redis:
        """
        Subscribes to a Redis channel.

        Args:
            chanel_id (str): Channel or chanel ID to subscribe to.

        Returns:
            aioredis.ChannelSubscribe: PubSub object for the subscribed channel.
        """
        redis_pubsub = await self.redis_connection.get_redis_pubsub()
        self.pubsub = await redis_pubsub.subscribe(chanel_id)
        return self.pubsub

    async def unsubscribe(self, chanel_id: str) -> None:
        """
        Unsubscribes from a Redis channel.

        Args:
            chanel_id (str): Channel or chanel ID to unsubscribe from.
        """
        redis_pubsub = await self.redis_connection.get_redis_pubsub()
        await redis_pubsub.unsubscribe(chanel_id)