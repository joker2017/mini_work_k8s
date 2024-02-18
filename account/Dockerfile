# Используем базовый образ Python 3.11 на Alpine Linux
FROM python:3.11-alpine AS builder

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /root

# Копируем файл с зависимостями проекта и устанавливаем зависимости
COPY requirements.txt .

# Установка зависимостей
RUN apk update && apk add --no-cache \
    curl \
    gcc \
    libc-dev \
    linux-headers \
    unit \
    unit-python3
RUN pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:3.10-alpine

WORKDIR /app

# Создаем директории для статических файлов и устанавливаем права доступа
#RUN mkdir -p /app/static/admin/{img,css,js} \
#    && mkdir -p /app/static/rest_framework/{img,css,js,fonts,docs} \
#    && chown -R unit:unit /app/static \
#    && chmod -R 777 /app/

COPY --chown=unit --from=builder /root/.local /opt/.local
ENV PATH=/opt/.local/bin:$PATH
ENV PYTHONPATH=/opt/.local/lib/python3.10/site-packages:$PYTHONPATH

COPY --chown=unit ./pdfsvc .
COPY ./unit.config.json /docker-entrypoint.d/ /docker-entrypoint.d/
COPY ./unit-docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/unit-docker-entrypoint.sh"]

# Определяем порт, который будет прослушивать приложение
EXPOSE 8300

#USER user
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
