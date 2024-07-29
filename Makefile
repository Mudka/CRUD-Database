.PHONY: install run migrate createsuperuser test

install:
	poetry install

run:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

createsuperuser:
	poetry run python manage.py createsuperuser

test:
	poetry run python manage.py test
