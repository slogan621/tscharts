FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY docker/requirements.txt /app/requirements.txt
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        python3-dev default-libmysqlclient-dev build-essential pkg-config \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

EXPOSE 8000
