
FROM python:3.9.13-alpine

WORKDIR /home/ubuntu/project


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . . 

RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev && \ 
    pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
