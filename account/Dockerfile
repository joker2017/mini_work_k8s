# Используем базовый образ Python 3.11 на Alpine Linux
FROM python:3.11-alpine

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка необходимых пакетов и добавление пользователя
RUN apk add --no-cache \
    # Добавляем необходимые пакеты для работы и компиляции зависимостей
    gcc \
    libc-dev \
    linux-headers \
    && adduser -D user

# Копируем файл с зависимостями проекта и устанавливаем зависимости
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копируем проект в контейнер
COPY . .

# Устанавливаем рабочую директорию
WORKDIR /app

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
    && chmod -R 755 /app/static

# Переключаемся на пользователя 'user'
USER user

# Удаляем файлы конфигурации по умолчанию и копируем наш файл конфигурации NGINX Unit
RUN rm -f /docker-entrypoint.d/*.json
COPY unit.config.json /docker-entrypoint.d/config.json

# Определяем порт, который будет прослушивать приложение
EXPOSE 8300

# Запускаем NGINX Unit
CMD ["unitd", "--no-daemon"]
