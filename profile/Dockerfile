# Установка базового образа Python
FROM python:3.11.0 as builder

# Установка переменных окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Установка системных зависимостей и зависимостей Python для сборки
RUN apt-get update && \
    apt-get install -y postgresql-client gcc libc-dev linux-headers postgresql-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
RUN pip install --upgrade pip --no-cache-dir
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Второй этап сборки для создания минимального образа
FROM python:3.11.0-slim

WORKDIR /app

# Копирование файлов из предыдущего этапа сборки
COPY --from=builder /app /app

# Установка NGINX Unit и модуля Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx-unit nginx-unit-python && \
    rm -rf /var/lib/apt/lists/*

# Создание пользователя для запуска приложения
RUN adduser --disabled-password --gecos '' user && chown -R user:user /app
USER user

# Копирование конфигурационного файла NGINX Unit
COPY unit.config.json /docker-entrypoint.d/

CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
