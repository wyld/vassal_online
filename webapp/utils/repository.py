import asyncio
import asyncio_mongo

import settings


loop = asyncio.get_event_loop()


class get_collection(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name

    async def __aenter__(self):
        self.mongo = await asyncio_mongo.Connection.create(
            settings.DB_HOST, settings.DB_PORT, loop=loop)
        database = getattr(self.mongo, settings.DB_NAME)
        return getattr(database, self.collection_name)

    async def __aexit__(self, type, value, traceback):
        await self.mongo.disconnect()
