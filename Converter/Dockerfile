FROM python:3.9-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev ffmpeg

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 converter.py