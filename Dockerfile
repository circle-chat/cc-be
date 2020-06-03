FROM python:3.8.3-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080

ENV PORT 8080

CMD exec gunicorn --bind :$PORT -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 circle:app
