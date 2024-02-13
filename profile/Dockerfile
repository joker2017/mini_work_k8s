# Используем официальный образ NGINX Unit для Python
FROM python:3.11-alpine as build-python
WORKDIR /app
#FROM unit:1.31.1-minimal
# Обновляем список пакетов и устанавливаем необходимые зависимости
RUN pip install --upgrade pip --no-cache-dir
COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir -v

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN apk del .tmp-build-deps
# Установка tree для просмотра структуры директорий, если необходимо

# Вывод структуры директорий
RUN ls -lah
# Или используйте tree для более детального представления
#RUN tree

#COPY requirements.txt /app/


COPY . /app

### Final image
FROM unit:1.31.1-python3.11
COPY --from=build-python /app /app

# Установка утилиты tree
RUN apt-get update && \
    apt-get install -y tree && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN tree
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY unit.config.json /docker-entrypoint.d/config.json


