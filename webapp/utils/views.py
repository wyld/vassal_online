import aiohttp.web
import aiohttp_jinja2
import ujson

import settings
from utils import cache


class BaseView(object):

    @classmethod
    def as_view(cls):
        return cls().dispatch

    async def dispatch(self, request):
        self.request = request
        context = await self.get_context(request)
        return await self.create_response(context)

    def create_response(self, context):
        return aiohttp.web.Response(context)


class TemplateResponseMixin(object):
    template = None

    async def create_response(self, context):
        if settings.DEBUG:
            return aiohttp_jinja2.render_template(
                self.template, self.request, context)

        html = await cache.cache_per_context(aiohttp_jinja2.render_string)(
            self.template, self.request, context, 
            app_key='aiohttp_jinja2_environment')
        response = aiohttp.web.Response()
        response.content_type = 'text/html'
        response.charset = 'utf-8'
        response.text = html
        return response


class TemplateView(TemplateResponseMixin, BaseView):
    pass


class JSONResponseMixin(object):
    content_type = 'application/json'

    async def create_response(self, context):
        json_response = ujson.dumps(context)
        return aiohttp.web.Response(
            body=bytes(json_response, 'utf8'),
            content_type=self.content_type)


class ApiView(JSONResponseMixin, BaseView):
    pass
