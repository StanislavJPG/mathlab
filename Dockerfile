FROM python:3.11
WORKDIR /mathlab

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /mathlab/

ENTRYPOINT [ "gunicorn", "core.wsgi", "-b", "0.0.0.0:8000"]