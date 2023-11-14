FROM python:3.11

WORKDIR /home/hasker/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN apt update; apt-get install libpcre3 libpcre3-dev -y
RUN pip3 install uwsgi -I

COPY .. .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD python /home/hasker/hasker/manage.py migrate
CMD uwsgi --ini /home/hasker/conf/uwsgi/uwsgi.ini