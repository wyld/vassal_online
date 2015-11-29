import asyncio
#import aioredis
import hashlib
import ujson

import settings


loop = asyncio.get_event_loop()


class get_connection(object):
    async def __aenter__(self):
        return await aioredis.create_redis(
            (settings.CACHE_HOST, settings.CACHE_PORT), loop=loop)

    async def __aexit__(self, type, value, traceback):
        self.redis.close()


async def read_cache(key):
    with get_connection() as redis:
        return await redis.get(key)


async def write_cache(key, value):
    with get_connection() as redis:
        return await redis.set(key, value)


CACHE = {}


def cache_per_context(func):
    async def _wrapper(template, request, context, **kwargs):
        key = hashlib.md5(ujson.dumps(context).encode('utf-8')).digest()
        value = CACHE.get(key)
        if not value:
            CACHE[key] = value = func(template, request, context, **kwargs)
        return value
    return _wrapper
