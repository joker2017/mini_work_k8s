# Используем базовый образ Python 3.11 на Alpine Linux
FROM python:3.11-alpine

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /root
# Установка зависимостей
RUN apk update && apk add --no-cache \
    curl \
    gcc \
    libc-dev \
    linux-headers \
    unit \
    unit-python3


# Копируем файл с зависимостями проекта и устанавливаем зависимости
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY docker-entrypoint.sh /tmp/
# Установка скрипта точки входа как исполняемого файла
#RUN chmod +x /tmp/docker-entrypoint.sh

# Удаляем файлы конфигурации по умолчанию и копируем наш файл конфигурации NGINX Unit
RUN rm -f /docker-entrypoint.d/*.json
COPY unit.config.json /docker-entrypoint.d/config.json

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем проект в контейнер
COPY . .

# Создаем директории для статических файлов и устанавливаем права доступа
RUN mkdir -p /app/static/admin/{img,css,js} \
    && mkdir -p /app/static/rest_framework/{img,css,js,fonts,docs} \
    && chown -R unit:unit /app/static \
    && chmod -R 777 /app/

# Определяем порт, который будет прослушивать приложение
EXPOSE 8300

# Настройка и запуск NGINX Unit при старте контейнера
ENTRYPOINT ["/tmp/docker-entrypoint.sh"]

# Переключаемся на пользователя 'user'
#USER user

