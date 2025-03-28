FROM python:3.11-slim-buster

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["python", "src"]