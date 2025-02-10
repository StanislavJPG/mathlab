
# for docker
up:
	docker-compose up

rebuild:
	docker-compose build --no-cache

soft-rebuild:
	docker-compose build

web:
	docker compose run --rm web sh
	#chmod +x manage.py

# for translation
makemessages:
	python manage.py makemessages -l en -l uk --ignore=private/node_modules/* --ignore=tmp/* --ignore=private/ --ignore=media/* --ignore=static/* --ignore=docs --ignore=docs_internal --add-location=file --no-obsolete

compilemessages:
	python manage.py compilemessages

