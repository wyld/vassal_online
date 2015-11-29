help:
	@echo 'Vassal-Online'
	@echo ''
	@echo 'Configuring:'
	@echo '   make setup        setup your machine for local development'
	@echo ''
	@echo 'Running'
	@echo '   make run          run the development servers'
	@echo ''
	@echo 'Testing'
	@echo '   make test         run unittests'

setup:
	virtualenv -p python3 env
	. env/bin/activate; \
	pip install -r requirements.txt

test:
	. env/bin/activate; \
	python -m unittest discover webapp.tests

run-server:
	. env/bin/activate; \
	python webapp/webapp.py

run:
	make run-server &
