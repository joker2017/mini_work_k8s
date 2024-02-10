# Используем официальный образ NGINX Unit для Python
FROM unit:1.31.1-python3.11

# Обновляем список пакетов и устанавливаем необходимые зависимости
# Например, gcc для компиляции некоторых Python пакетов
RUN apt-get update && \
    apt-get install -y gcc && \
    # Очищаем кэш apt для уменьшения размера образа
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию для приложения
WORKDIR /www/app

# Копируем файлы приложения в контейнер
COPY . .

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем конфигурационный файл NGINX Unit для автоматической настройки
COPY unit.config.json /docker-entrypoint.d/config.json

# Определяем порт, который будет прослушивать приложение
EXPOSE 80

# Команда запуска NGINX Unit уже определена в базовом образе,
# поэтому здесь не требуется указывать CMD или ENTRYPOINT.



