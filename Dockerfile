FROM python:3.10.0-alpine

WORKDIR opt/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
ADD db.sqlite db.sqlite
ADD load_data.py load_data.py


RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN apk add --no-cache --virtual .build-deps \
    bash ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev curl\
    && apk add --no-cache netcat-openbsd \
    && pip install --no-cache-dir -r requirements.txt


COPY . .

RUN chmod +x /opt/app/entrypoint.sh && chmod +x /opt/app/load_data.py

ENTRYPOINT ["./entrypoint.sh"]
