# Используем базовый образ Python с Alpine для сборки
FROM python:3.10.0 as builder

# Установка переменных окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Установка зависимостей Python и системных зависимостей для сборки
RUN apk update && apk add --no-cache postgresql-client jpeg-dev nginx-unit nginx-unit-python && \
    apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

COPY ./requirements.txt .
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

# Копирование оставшихся файлов проекта
COPY . .

# Очищаем временные зависимости
RUN apk del .tmp-build-deps

# Второй этап сборки для создания минимального образа
FROM python:3.10.0-alpine

WORKDIR /app
COPY --from=builder /app /app

# Установка NGINX Unit и модуля Python
RUN apk add --no-cache nginx-unit nginx-unit-python

# Создание пользователя для запуска приложения
RUN adduser -D user && chown -R user:user /app
USER user

# Копируем конфигурацию NGINX Unit
COPY unit.config.json /docker-entrypoint.d/

# Настройка точки входа для запуска NGINX Unit с нашей конфигурацией
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]

