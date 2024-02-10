# Используем базовый образ Python с Alpine для сборки
FROM python:3.10.0 as builder

# Установка переменных окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Установка зависимостей Python и системных зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libjpeg-dev \
    nginx-unit \
    nginx-unit-python \
    gcc \
    libc-dev \
    linux-headers \
    libpq-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

# Копирование оставшихся файлов проекта
COPY . .

# Второй этап сборки для создания минимального образа
FROM python:3.10.0-slim

WORKDIR /app
COPY --from=builder /app /app

# Установка NGINX Unit и модуля Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx-unit \
    nginx-unit-python && \
    rm -rf /var/lib/apt/lists/*

# Создание пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' user && chown -R user:user /app
USER user

# Копируем конфигурацию NGINX Unit
COPY unit.config.json /docker-entrypoint.d/

# Настройка точки входа для запуска NGINX Unit с нашей конфигурацией
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
