FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip


COPY ../requirements.txt ./
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD python hasker/manage.py migrate
CMD python hasker/manage.py runserver