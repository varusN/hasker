FROM python:3.10

WORKDIR /home/hasker/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN unset PYTHONPATH
RUN unset PYTHONHOME

RUN mkdir /sock
RUN chmod -R 666 /sock
COPY ./conf/uwsgi/uwsgi.ini /etc/

RUN pip3 install --upgrade pip
RUN apt update; apt-get install libpcre3 libpcre3-dev -y
RUN pip3 install uwsgi -I

COPY .. .
RUN pip3 install -Ur requirements.txt
