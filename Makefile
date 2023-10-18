install-req:
	poetry install

migration-up:
	alembic upgrade head

compose-up:
	docker-compose up --build -d

compose-down:
	docker-compose down

db-with-migration:
	docker-compose up --build -d database migration

run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8080