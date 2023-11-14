FROM python:3.11

WORKDIR /home/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip \
RUN apt-get install libpcre3 libpcre3-dev
pip3 install uwsgi -I

COPY .. .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD python /home/hasker/manage.py migrate
CMD uwsgi --ini home/hasker/conf/uwsgi.ini