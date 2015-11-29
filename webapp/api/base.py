import repository
from utils.views import ApiView


class ListResource(ApiView):
	async def get_context(self, request):
		objects = await self.repository.objects_filter()
		return {'objects': objects, 'total': len(objects)}
