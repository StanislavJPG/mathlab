## Використовуємо офіційний Python-образ
#FROM python:3.10.12
#
## Встановлюємо необхідні пакети та Poetry
#RUN apt-get update && apt-get install --no-install-recommends -y curl \
#    && curl -sSL https://install.python-poetry.org | python3 - \
#    && rm -rf /var/lib/apt/lists/*
#
## Додаємо Poetry в глобальний PATH
#ENV POETRY_HOME="/root/.local"
#ENV PATH="$POETRY_HOME/bin:$PATH"
#
## Встановлюємо робочу директорію
#WORKDIR /home/dev/mathlab
#
## Копіюємо файли залежностей
#COPY README.md pyproject.toml poetry.lock /home/dev/mathlab/
#
## Встановлюємо залежності через Poetry
#RUN poetry install
#
## Копіюємо весь проект
#COPY . /home/dev/mathlab/
#
## Відкриваємо порт
#EXPOSE 8000
#
## Запускаємо Django
##CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# The base image we want to inherit from
FROM python:3.10.12

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=2.0.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /mathlab
COPY pyproject.toml poetry.lock /mathlab/

# Install dependencies:
RUN poetry install --no-root
# copy project
COPY . .