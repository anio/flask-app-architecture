

.ONESHELL:

FLASK_APP := main.py
export FLASK_APP


init:
	@virtualenv venv
	@source venv/bin/activate
	@python -m pip install -r requirements.txt

migrate:
	@echo Migrating...
	@source venv/bin/activate
	@cd app
	@python -m flask db init
	@python -m flask db migrate
	# @python -m flask db heads
	# @python -m flask db stamp
	@python -m flask db upgrade

run:
	@echo Starting in development ENV...
	@source venv/bin/activate
	@cd app
	@FLASK_ENV=development python -m flask run -p 8080

production:
	@echo Starting in development ENV...
	@source venv/bin/activate
	@cd app
	@uwsgi --http 127.0.0.1:8080 --wsgi-file main.py --callable app -L
