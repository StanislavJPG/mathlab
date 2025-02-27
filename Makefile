
# for docker
up:
	docker-compose up

rebuild:
	docker-compose up --build

build:
	docker-compose build

web:
	docker-compose run --rm web bash

# for translation
makemessages:
	python manage.py makemessages -l en -l uk --ignore=media/* --ignore=static/* --ignore=docs --add-location=file --no-obsolete

js-makemessages:
	python manage.py makemessages -l en -l uk -d djangojs

compilemessages:
	python manage.py compilemessages

