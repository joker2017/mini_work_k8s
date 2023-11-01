FROM python:3.10.0-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#WORKDIR ./

FROM python:3.10.0-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
## create the app user
#RUN addgroup --system app && adduser --system --group app
COPY ./app ./
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /app/requirements.txt --no-cache-dir

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN apk del .tmp-build-deps

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 777 /vol/web
#RUN chown -R 999:999 /app/account/migrations
#RUN chown -R 999 /app/account/migrations
USER user
#CMD ["gunicorn", "app.wsgi:application", "--bind" "0.0.0.0:8000"]
#ENTRYPOINT ["/app/entrypoint.sh"]
ENTRYPOINT ["/account/entrypoint.sh"]