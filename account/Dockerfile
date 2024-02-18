# Используем базовый образ Python 3.11 на Alpine Linux
FROM python:3.11-alpine AS builder

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /root

# Копируем файл с зависимостями проекта и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Установка зависимостей
RUN apk update && apk add --no-cache \
    curl \
    gcc \
    libc-dev \
    linux-headers


# Final image
FROM python:3.11-alpine

WORKDIR /opt/app

# Создаем директории для статических файлов и устанавливаем права доступа
#RUN mkdir -p /app/static/admin/{img,css,js} \
#    && mkdir -p /app/static/rest_framework/{img,css,js,fonts,docs} \
#    && chown -R unit:unit /app/static \
#    && chmod -R 777 /app/
RUN apk add --no-cache unit unit-python3 curl

COPY --chown=unit --from=builder /root/.local /opt/.local
ENV PATH=/opt/.local/bin:$PATH
ENV PYTHONPATH=/opt/.local/lib/python3.11/site-packages:$PYTHONPATH

COPY --chown=unit ./app .
COPY ./django.unit.json ./django-entrypoint.sh /docker-entrypoint.d/
COPY ./unit-docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/unit-docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.d/django-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/unit-docker-entrypoint.sh"]

# Определяем порт, который будет прослушивать приложение
EXPOSE 8300

#USER user
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
