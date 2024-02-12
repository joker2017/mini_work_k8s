# Используем официальный образ NGINX Unit для Python
FROM python:3.11-alpine
#FROM unit:1.31.1-minimal
# Обновляем список пакетов и устанавливаем необходимые зависимости
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Установка tree для просмотра структуры директорий, если необходимо
RUN apt-get update && apt-get install -y tree && apt-get clean
# Вывод структуры директорий
RUN ls -lah
# Или используйте tree для более детального представления
RUN tree

#COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

### Final image
FROM unit:1.31.1-python3.11
COPY --from=build-python /app /app
RUN tree
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY unit.config.json /docker-entrypoint.d/config.json


