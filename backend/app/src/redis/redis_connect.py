import asyncio
from typing import Any
from redis.asyncio.client import PubSub , Redis as RedisAsync
from redis import Redis as RedisSync, exceptions
import redis.asyncio as Redis

class RedisConnect():
    
    def __init__(self, host='localhost', port=6379, redis_url='redis://redis-local:6379'):
        self.redis_url = redis_url
        self.redis_host = host
        self.redis_port = port
        self.redis_sync: RedisSync | None = None
        self.redis_async: RedisAsync | None = None
        
    async def is_redis_async_available(self) -> bool:
        try:
            if self.redis_async is None:
                self.redis_async = await self._get_async_redis_connection()
                
            pong = self.redis_async.ping()
            print("Successfully connected to RedisAsync", pong)
        except (exceptions.ConnectionError, ConnectionRefusedError) as error:
            print("RedisAync connection error!", error)
            return False
        return True
    
    def is_redis_sync_available(self):
        try:
            if self.redis_sync is None:
                self.redis_sync = self._get_sync_redis_connection()
            pong = self.redis_sync.ping()
            print("Successfully connected to RedisSync", pong)
        except (exceptions.ConnectionError, ConnectionRefusedError) as error:
            print("RedisSync connection error!", error)
            return False
        return True
    
    
    def _get_sync_redis_connection(self):
        self.redis_sync = RedisSync.from_url(self.redis_url)
        return self.redis_sync
        
        
    async def _get_async_redis_connection(self) -> RedisAsync:
        """ Установка соединения с Redis.
        Returns:
            aioredis.Redis: Redis connection object.
        """
        self.redis_async = Redis.from_url(url=self.redis_url)
        await self.redis_async.set(name="R", value=1)
        pong = self.is_redis_async_available()
        return self.redis_async
            
    async def get_redis_connection(self) -> RedisAsync:
        # if await self.is_redis_async_available():
        #     print("get_redis_connection")
        redis_async = await self._get_async_redis_connection()
        return redis_async


    async def get_redis_pubsub(self) -> PubSub:
        # if (await self.is_redis_async_available()):
        #     print("get_redis_pubsub")
        redis_async = await self._get_async_redis_connection()
        return redis_async.pubsub
        