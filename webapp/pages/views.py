from utils.views import TemplateView


class HomePage(TemplateView):
	template = 'index.html'

	async def get_context(self, request):
		return {}
