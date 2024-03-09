import asyncio
from typing import Any
from redis.asyncio.client import PubSub, Redis

class RedisConnect():
    
    def __init__(self, host='localhost', port=6379):
        self.redis_host = host
        self.redis_port = port
        self.redis_connection: Redis | None = None
        self.redis_pubsub: PubSub
        
    async def _test_redis_connection(self) -> None:
        try:
            
            if self.redis_connection:
                await self.redis_connection.ping()

            assert self.redis_connection == None, f"redis_connection is None"
        except Exception as error:
            print(error)
        
    async def _get_redis_connection(self) -> Redis:
        """
        Establishes a connection to Redis.

        Returns:
            aioredis.Redis: Redis connection object.
        """
        redis_connection = Redis(host=self.redis_host,
                              port=self.redis_port,
                              auto_close_connection_pool=False)
        
        await self._test_redis_connection()
        
        return redis_connection

    async def connect(self) -> None:
        """
        Connects to the Redis server and initializes the pubsub client.
        """
        if not self.redis_connection:
            self.redis_connection = await self._get_redis_connection()
            self.redis_pubsub = self.redis_connection.pubsub()
            
    async def get_redis_connection(self) -> Redis:
        if self.redis_connection is None:
            await self.connect()
        
        return self.redis_connection
    
    async def get_redis_pubsub(self) -> PubSub:
        if self.redis_connection is None:
            await self.connect()
        
        return self.redis_pubsub