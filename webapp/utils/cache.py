import asyncio
import aioredis
import hashlib
from functools import wraps
import ujson

import settings


loop = asyncio.get_event_loop()


class get_connection(object):
    async def __aenter__(self):
        self.redis = await aioredis.create_redis(
            (settings.CACHE_HOST, settings.CACHE_PORT), loop=loop)
        return self.redis

    async def __aexit__(self, type, value, traceback):
        self.redis.close()


async def read_cache(key):
    async with get_connection() as redis:
        return await redis.get(key)


async def write_cache(key, value):
    async with get_connection() as redis:
        return await redis.set(key, value)


async def clear_cache(key):
    async with get_connection() as redis:
        return await redis.delete(key)


def cache_per_context(func):
    @wraps(func)
    async def _wrapper(template, request, context, **kwargs):
        key = '{}={}'.format(
            func.__name__, 
            hashlib.md5(ujson.dumps(context).encode('utf-8')).digest())

        value = await read_cache(key)
        if isinstance(value, bytes):
            value = value.decode('utf-8')

        if not value:
            value = func(template, request, context, **kwargs)
            await write_cache(key, value)
        return value
    return _wrapper
