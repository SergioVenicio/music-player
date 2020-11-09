FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apk update \
    && apk add \
    build-base postgresql-dev gcc zlib-dev jpeg-dev
COPY . /code/
RUN chmod +x /code/entrypoint.sh
RUN pip install --upgrade pip && pip install -r requirements.txt
ENTRYPOINT ["sh", "/code/entrypoint.sh"]