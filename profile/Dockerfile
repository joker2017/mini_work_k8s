# Установка базового образа Python с Alpine для сборки
FROM python:3.10.11 as builder

# Установка переменных окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Установка системных зависимостей и зависимостей Python для сборки
RUN apk update && apk add --no-cache \
    postgresql-client \
    jpeg-dev \
    gcc \
    libc-dev \
    linux-headers \
    musl-dev \
    zlib-dev \
    nginx-unit \
    nginx-unit-python

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей Python
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
# COPY . .

# Второй этап сборки для создания минимального образа
FROM python:3.10.11-slim

# Создание рабочей директории
WORKDIR /app

# Копирование файлов из предыдущего этапа сборки
COPY --from=builder /app /app

# Установка NGINX Unit и модуля Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx-unit \
    nginx-unit-python && \
    rm -rf /var/lib/apt/lists/*

# Создание пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' user && chown -R user:user /app
USER user

# Копирование конфигурационного файла NGINX Unit
COPY unit.config.json /docker-entrypoint.d/

# Настройка точки входа для запуска NGINX Unit с нашей конфигурацией
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
