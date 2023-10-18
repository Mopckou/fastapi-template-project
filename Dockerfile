FROM python:3.10.12-alpine as build

RUN apk add --no-cache bash curl
SHELL ["bash", "-c"]

WORKDIR workdir

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.5.0 POETRY_HOME=/opt/poetry python -
ENV PATH=${HOME}/opt/poetry/bin:${PATH}
ENV PYTHONUNBUFFERED=1

COPY poetry.lock pyproject.toml /workdir/
RUN poetry config virtualenvs.create false && poetry install
COPY . /workdir/

EXPOSE 8080

CMD ["/opt/poetry/bin/poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
