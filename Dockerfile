FROM python:3.8.3-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . ./

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers=2 --threads=8 --timeout=0 --worker-class=eventlet --worker-class=gthread circle:app