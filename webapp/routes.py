from api import games, modules
from pages import views


urls = (
	('GET', '/', views.HomePage.as_view()),

	('GET', '/api/games/', games.GamesList.as_view()),
	('GET', '/api/modules/', modules.ModulesList.as_view()),
    ('POST', '/api/modules/import/', modules.ModulesImport.as_view()),
)
