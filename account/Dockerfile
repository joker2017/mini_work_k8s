#FROM nginx/unit:1.26.1-python3.9
FROM unit:1.31.1-python3.11

RUN ls -lah
WORKDIR /app
# Установка зависимостей проекта
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копирование проекта в контейнер
COPY . .

# Настройка рабочего каталога
#WORKDIR /app
RUN chown -R unit:unit ./
RUN mkdir -p /vol/web/static/

# Команда для сбора статических файлов Django
#RUN python app/manage.py collectstatic --noinput

# Выставление прав доступа
RUN chown -R unit:unit ./
RUN mkdir -p /vol/web/static/
RUN ls -lah
# Удаление файла конфигурации по умолчанию и копирование нашей конфигурации
RUN rm -f /docker-entrypoint.d/*.json
COPY unit.config.json /docker-entrypoint.d/config.json
# Определяем порт, который будет прослушивать приложение
EXPOSE 8300