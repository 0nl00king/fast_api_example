FROM docker.stm/python:3.9-alpine

ADD ./requirements.txt /tmp/requirements.txt
WORKDIR /code

RUN apk update
RUN apk add --no-cache g++ \
    musl-dev \
    linux-headers \
    zlib-dev \
    jpeg-dev \
    python3-dev \
    ffmpeg \
    postgresql-dev \
    postgresql-client

RUN pip install --upgrade pip

RUN pip install -r /tmp/requirements.txt --force-reinstall --upgrade --no-cache-dir

RUN addgroup --gid 1000 --system web && adduser --system -G web --uid 1000 web

USER web