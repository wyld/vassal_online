from contextlib import closing
import io

from repository import modules
from api.base import ListResource
from api.parsers.module import ModuleParser
from utils.exceptions import ValidationError
from utils.views import ApiView


class ModulesList(ListResource):
	repository = modules


class ModulesImport(ApiView):
    async def get_context(self, request):
        post_data = await request.post()
        filename = post_data['module'].filename
        input_file = post_data['module'].file

        with closing(io.BytesIO(input_file.read())) as module_file:
            parser = ModuleParser(module_file)

            try:
                module = parser.extract()
            except ValidationError as e:
                return {'error': str(e)}

            await modules.objects_replace(module)
        return {'object': module}
