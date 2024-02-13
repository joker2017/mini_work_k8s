# Используем официальный образ NGINX Unit для Python
FROM unit:1.31.1-python3.11
#FROM unit:1.31.1-minimal
# Обновляем список пакетов и устанавливаем необходимые зависимости
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию для приложения
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . .
RUN chown -R unit:unit /app

# Установка tree для просмотра структуры директорий, если необходимо
RUN apt-get update && apt-get install -y tree && apt-get clean
# Вывод структуры директорий
RUN ls -lah
# Или используйте tree для более детального представления
RUN tree



# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем конфигурационный файл NGINX Unit для автоматической настройки
COPY unit.config.json /docker-entrypoint.d/config.json
# Выполняем команду collectstatic для Django
# Обратите внимание, что вы должны настроить Django на использование файловой системы для статических файлов
# Это может потребовать изменения в settings.py вашего приложения Django
RUN mkdir -p /vol/web/static
RUN python app/manage.py collectstatic --no-input
# Указываем пути для статических файлов и медиа
#VOLUME ["/vol/web"]

# Определяем порт, который будет прослушивать приложение
EXPOSE 8300