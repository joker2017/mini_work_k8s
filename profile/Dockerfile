#FROM nginx/unit:1.26.1-python3.9
FROM unit:1.31.1-python3.11

RUN ls -lah
#
# Установка зависимостей проекта
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копирование проекта в контейнер
COPY . .

# Настройка рабочего каталога
#WORKDIR /app
# Выставление прав доступа

RUN mkdir -p app/static/
#RUN chown -R unit:unit ./
COPY /unit.config.json /docker-entrypoint.d/config.json
# Команда для сбора статических файлов Django
#RUN python app/manage.py collectstatic --noinput
WORKDIR /app
#RUN mkdir -p /vol/web/static/
RUN ls -lah \
RUN chown -R unit:unit /app
# Удаление файла конфигурации по умолчанию и копирование нашей конфигурации
RUN rm -f /docker-entrypoint.d/*.json
COPY docker-entrypoint.sh /docker-entrypoint.sh
# Установка скрипта точки входа как исполняемого файла
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

#RUN chown -R unit:unit app/static/
# Определяем порт, который будет прослушивать приложение
EXPOSE 8300