# pull official base image
FROM python:3.9.13-alpine

MAINTAINER Nikoloz Naskidashvili <nikoloz2005@gmail.com>

# set work directory
WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG FLASK_ENV
ARG FLASK_APP

ENV GROUP_ID=1000 \
    USER_ID=1000

# install dependencies
RUN python -m pip install -U --force-reinstall pip
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev vim \
#    && apk add --virtual build-deps build-base gcc musl-dev jpeg-dev zlib-dev && \
#    && apk add postgresql-dev \
    && rm -rf /var/cache/apk/*

COPY ./requirements.txt ./requirements.txt
COPY ./requirements ./requirements

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN flask digest compile

# copy project
COPY . .

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

EXPOSE 5000

USER www

ENTRYPOINT [
      "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "manage:application", "-k", "gevent", "--timeout", "300",
      "--worker-connections", "1000", "--max-requests", "1000000", "--limit-request-line", "8190",
      "--access-logfile", "'-'", "--error-logfile", "'-'"
    ]