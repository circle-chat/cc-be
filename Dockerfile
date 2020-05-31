FROM python:3.8.3-buster
# RUN pip install poetry
# WORKDIR /circle-chat
# COPY poetry.lock pyproject.toml /circle-chat/
# RUN mkdir /circle-chat/lib && touch /circle-chat/lib/__init__.py
# RUN cd /tmp && poetry install --no-root
# Copy in everything else:
# COPY . .
# RUN poetry install --no-interaction
# COPY . /circle-chat


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD flask run