# Первый этап: Сборка и установка зависимостей Python
FROM python:3.11.0 as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Установка системных и Python зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Второй этап: Создание конечного образа с NGINX Unit
FROM python:3.11.0-slim

WORKDIR /app

# Копирование файлов из первого этапа сборки
COPY --from=builder /app /app

# Установка NGINX Unit и модуля Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg1 lsb-release curl && \
    echo "deb https://packages.nginx.org/unit/debian/ $(lsb_release -cs) unit" > /etc/apt/sources.list.d/unit.list && \
    echo "deb-src https://packages.nginx.org/unit/debian/ $(lsb_release -cs) unit" >> /etc/apt/sources.list.d/unit.list && \
    curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - && \
    apt-get update && \
    apt-get install -y unit unit-python && \
    rm -rf /var/lib/apt/lists/*

# Создание пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' user && chown -R user:user /app
USER user

# Копирование конфигурационного файла NGINX Unit
COPY unit.config.json /docker-entrypoint.d/

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
