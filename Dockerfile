FROM python:3

RUN mkdir /app
COPY . /app

WORKDIR /app

RUN pip install poetry
RUN poetry install

CMD ["sleep", "infinity"]
