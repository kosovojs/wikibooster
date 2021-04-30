FROM python:3.7
WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1
