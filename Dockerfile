FROM python:3.11

COPY ../requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ../hasker .
