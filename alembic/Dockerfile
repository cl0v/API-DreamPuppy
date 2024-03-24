FROM python:3.12-slim

WORKDIR /alembic

COPY requirements.txt .
COPY src src
COPY alembic.ini .

RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

ENTRYPOINT alembic upgrade head