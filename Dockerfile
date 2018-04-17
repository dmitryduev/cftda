FROM python:3.6
LABEL maintainer="duev@caltech.edu"

ENV PYTHONUNBUFFERED 1
#ENV DJANGO_ENV dev
#ENV DJANGO_SETTINGS_MODULE "cftda.settings.dev"
ENV DJANGO_ENV production
ENV DJANGO_SETTINGS_MODULE "cftda.settings.production"

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

COPY . /code/
WORKDIR /code/

RUN mkdir /cftda-db
#COPY ./db.sqlite3 /cftda-db/
RUN mkdir /cftda-media

RUN python manage.py migrate

#RUN useradd wagtail
#RUN chown -R wagtail /code
#USER wagtail

EXPOSE 8005
CMD exec gunicorn cftda.wsgi:application --bind 0.0.0.0:8005 --workers 4
