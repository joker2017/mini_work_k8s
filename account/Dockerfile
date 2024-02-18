# Используем базовый образ Python 3.11 на Alpine Linux
FROM python:3.11-alpine

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка зависимостей
RUN apk update && apk add --no-cache \
    curl \
    gcc \
    libc-dev \
    linux-headers \
    && adduser -D user \
    && mkdir -p /var/lib/unit \
    && chown -R user:user /var/lib/unit \
    && chmod -R 755 /var/lib/unit



# Добавление официального ключа NGINX и настройка репозитория для Alpine
# Добавление официального ключа NGINX и настройка репозитория для Alpine
RUN curl -O https://nginx.org/keys/nginx_signing.rsa.pub \
    && mv nginx_signing.rsa.pub /etc/apk/keys/ \
    && printf "@nginx https://nginx.org/packages/mainline/alpine/v%s/main\n" $(egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release) | tee -a /etc/apk/repositories \
    && apk add unit@nginx unit-python3@nginx



# Копируем файл с зависимостями проекта и устанавливаем зависимости
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копируем проект в контейнер
COPY . .



# Создаем директории для статических файлов и устанавливаем права доступа
RUN mkdir -p /app/static/admin/img \
    && mkdir -p /app/static/admin/css \
    && mkdir -p /app/static/admin/js \
    && mkdir -p /app/static/rest_framework/img \
    && mkdir -p /app/static/rest_framework/css \
    && mkdir -p /app/static/rest_framework/js \
    && mkdir -p /app/static/rest_framework/fonts \
    && mkdir -p /app/static/rest_framework/docs \
    && chown -R user:user /app/static \
    && chmod -R 777 /app/static



# Удаляем файлы конфигурации по умолчанию и копируем наш файл конфигурации NGINX Unit
RUN rm -f /docker-entrypoint.d/*.json
COPY unit.config.json /docker-entrypoint.d/config.json
# Устанавливаем рабочую директорию
WORKDIR /app

# Определяем порт, который будет прослушивать приложение
EXPOSE 8300
# Запускаем NGINX Unit
# Настройка и запуск NGINX Unit при старте контейнера
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
# Переключаемся на пользователя 'user'
#USER user