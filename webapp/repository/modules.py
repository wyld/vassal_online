from utils.repository import get_collection


COLLECTION_NAME = 'modules'


async def objects_all():
	return await objects_filter()


async def objects_filter(**kwargs):
	async with get_collection(COLLECTION_NAME) as collection:
		return await collection.find()
