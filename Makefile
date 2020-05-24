test:
	python3 -m pytest --junitxml=report.xml --cov-report=xml --cov=.

upgrade_db:
	alembic -c src/app/infrastructure/alembic/alembic.ini --raiseerr upgrade heads

migration:
	alembic -c src/app/infrastructure/alembic/alembic.ini revision --autogenerate -m $(comment)

