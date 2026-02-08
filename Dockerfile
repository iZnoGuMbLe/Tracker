FROM python:3.12.10-slim

RUN pip install poetry==1.7.1

WORKDIR /app


COPY pyproject.toml poetry.lock* ./


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main


COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
