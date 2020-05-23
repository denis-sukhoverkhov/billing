test:
	sh ./.ci-cd/test.sh pfr $(commit)

upgrade_db:
	alembic -c src/app/infrastructure/alembic/alembic.ini --raiseerr upgrade heads

migration:
	alembic -c src/app/infrastructure/alembic/alembic.ini revision --autogenerate -m $(comment)

main_handler:
	python manage.py main_handler

pfr_response_handler:
	python manage.py pfr_response_handler

requirements:
	pipenv lock --clear
	pipenv install --dev
	pip install -e ./src
