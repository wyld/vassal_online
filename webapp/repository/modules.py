from utils.repository import get_collection


COLLECTION_NAME = 'modules'


async def objects_all():
	return await objects_filter()


async def objects_filter(**kwargs):
	async with get_collection(COLLECTION_NAME) as collection:
		return await collection.find()


async def objects_replace(item):
    async with get_collection(COLLECTION_NAME) as collection:
        await collection.remove({'_id': item.get('_id')})
        return await collection.insert(item)
