FROM python:3.11

ENV DockerHome=/home/app/hasker

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD python manage.py migrate
CMD python manage.py runserver