# Первый этап: Сборка и установка зависимостей Python
FROM python:3.11.0 as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

 #COPY . .

# Второй этап: Создание конечного образа с NGINX Unit
FROM debian:buster-slim

WORKDIR /app

# Скачивание и сохранение ключа подписи NGINX и добавление репозитория Unit
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg1 curl && \
    curl --insecure --output /usr/share/keyrings/nginx-keyring.gpg https://unit.nginx.org/keys/nginx-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ buster unit" > /etc/apt/sources.list.d/unit.list && \
    echo "deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ buster unit" >> /etc/apt/sources.list.d/unit.list && \
    apt-get update && \
    apt-get install -y unit unit-python3.7 && \
    rm -rf /var/lib/apt/lists/*


# Копирование приложения и зависимостей из первого этапа
COPY --from=builder /app /app

# Создание пользователя для запуска приложения
RUN useradd --create-home appuser
USER appuser

# Копирование конфигурационного файла NGINX Unit (если он необходим)
COPY --from=builder /app/unit.config.json /docker-entrypoint.d/unit.config.json

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
