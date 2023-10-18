# Fastapi-template-project

# Features
- Async FastApi
- Async SQLAlchemy session
- Async python-dependency-injector

## Installation
[Install](<https://python-poetry.org/docs/#installation>)  poetry. Check version:
```
poetry --version
```

Create virtualenv and install requirements:
```
poetry install
```

## Run
Run with docker-compose:
```
make compose-up
```
---
Or first we launch the database with migration:
```
make db-with-migration
```

And run server:
```
make run
```
---
Make a request:
```
curl -i http://0.0.0.0:8080/v1/users
```