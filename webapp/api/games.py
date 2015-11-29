from repository import games
from api.base import ListResource


class GamesList(ListResource):
	repository = games
