# Pull base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y g++ gcc

WORKDIR /code
RUN mkdir -p /code/app
COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD  /code/run.sh