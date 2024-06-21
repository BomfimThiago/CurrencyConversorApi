FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install --yes libmagic-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD src/core/config/requirements/base.txt ./src/core/config/requirements.txt
RUN  python -m pip install -U pip && pip install -r src/core/config/requirements.txt
COPY . /usr/src/app

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
