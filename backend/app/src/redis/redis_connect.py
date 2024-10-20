# import asyncio
# from typing import Any
# from redis.asyncio.client import PubSub , Redis as RedisAsync
from redis import Redis as RedisSync, exceptions
# import redis.asyncio as Redis
import aioredis
from aioredis import Redis as RedisAsync
from aioredis.client import PubSub
from app.src.core.logging import logger

class RedisConnect():
    
    def __init__(self, host='localhost', port=6379, redis_url='redis://redis-test:6379'):
        self.redis_url = redis_url
        self.redis_host = host
        self.redis_port = port
        self.redis_sync: RedisSync | None = None
        self.redis_async: RedisAsync | None = None
        logger.info(f"Created RedisConnec {self.redis_url}")
        
    async def is_redis_async_available(self) -> bool:
        try:
            if self.redis_async is None:
                self.redis_async = await self._get_async_redis_connection()
            else:
                pong = await self.redis_async.ping()
                logger.info("Successfully connected to RedisAsync", pong)
        except (exceptions.ConnectionError, ConnectionRefusedError) as error:
            logger.error("RedisAync connection error!", error)
            return False
        return True
    
    def is_redis_sync_available(self):
        try:
            if self.redis_sync is None:
                self.redis_sync = self._get_sync_redis_connection()
            pong = self.redis_sync.ping()
            logger.info("Successfully connected to RedisSync", pong)
        except (exceptions.ConnectionError, ConnectionRefusedError) as error:
            logger.info("RedisSync connection error!", error)
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
        self.redis_async = aioredis.from_url(url=self.redis_url)
        pong = await self.redis_async.ping()
        logger.info(f"get_async_redis_connection, pong {pong}")
        return self.redis_async
            
    async def get_redis_connection(self) -> RedisAsync:
        # if await self.is_redis_async_available():
        logger.info("get_redis_connection")
        redis_async = await self._get_async_redis_connection()
        return redis_async


    async def get_redis_pubsub(self) -> PubSub:
        # if (await self.is_redis_async_available()):
        logger.info("get_redis_pubsub")
        redis_async = await self._get_async_redis_connection()
        return redis_async.pubsub()
        