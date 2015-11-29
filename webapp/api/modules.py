from repository import modules
from api.base import ListResource


class ModulesList(ListResource):
	repository = modules
