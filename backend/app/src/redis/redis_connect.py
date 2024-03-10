import asyncio
from typing import Any
from redis.asyncio.client import PubSub, Redis as RedisAsync
from redis import Redis as RedisSync, exceptions

class RedisConnect():
    
    def __init__(self, host='localhost', port=6379, redis_url='redis://redis-local:6379/0'):
        self.redis_url = redis_url
        self.redis_host = host
        self.redis_port = port
        self.redis_sync: RedisSync | None = None
        self.redis_async: RedisAsync | None = None
        self.redis_pubsub: PubSub
        
    async def is_redis_async_available(self) -> bool:
        try:
            if not self.redis_async:
                await self._get_async_redis_connection()
                
            pong = await self.redis_async.ping()
            print("Successfully connected to RedisAsync", pong)
        except (exceptions.ConnectionError, ConnectionRefusedError) as error:
            print("RedisAync connection error!", error)
            return False
        return True
    
    def is_redis_sync_available(self):
        try:
            if not self.redis_sync:
                self._get_sync_redis_connection()
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
        """
        Establishes a connection to Redis.

        Returns:
            aioredis.Redis: Redis connection object.
        """
        # self.redis_async = RedisAsync(host=self.redis_host,
        #                       port=self.redis_port,
        #                       auto_close_connection_pool=False)
        self.redis_async = RedisAsync.from_url(self.redis_url)    
        self.redis_pubsub = self.redis_async.pubsub()
      
        return self.redis_async
         
            
    async def get_redis_connection(self) -> RedisAsync:
        if (await self.is_redis_async_available()):
            print("get_redis_connection")
        return self.redis_async


    async def get_redis_pubsub(self) -> PubSub:
        if (await self.is_redis_async_available()):
            print("get_redis_pubsub")
        return self.redis_pubsub
        