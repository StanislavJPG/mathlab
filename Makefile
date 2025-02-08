
# for docker
make up:
	docker-compose up

make rebuild:
	docker-compose build --no-cache

make web:
	docker compose run --rm web sh
	#chmod +x manage.py

# for translation
make makemessages:
	python manage.py makemessages -l en -l uk --ignore=private/node_modules/* --ignore=tmp/* --ignore=private/ --ignore=media/* --ignore=static/* --ignore=docs --ignore=docs_internal --add-location=file --no-obsolete

make compilemessages:
	python manage.py compilemessages

