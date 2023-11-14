FROM python:3.11

COPY ../requiriments.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY .. .
