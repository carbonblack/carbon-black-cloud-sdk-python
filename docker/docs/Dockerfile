FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    && apt-get install -y texlive \
    && apt-get install -y texlive-latex-extra \
    && apt-get install -y dvipng \
    && apt-get install -y python3-sphinx \
    # Translations dependencies
    && apt-get install -y gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . /app

RUN pip install --no-input Sphinx sphinx-autobuild sphinx-rtd-theme \
    && pip install -r app/docs/requirements.txt \
    && pip install /app

WORKDIR /app/docs/
