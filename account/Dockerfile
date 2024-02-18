#FROM nginx/unit:1.26.1-python3.9
FROM unit:1.31.1-python3.11
#
# Установка зависимостей проекта
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копирование проекта в контейнер
COPY . .

# Настройка рабочего каталога
#WORKDIR /app
# Выставление прав доступа
RUN mkdir -p /app/static/admin/img
RUN mkdir -p /app/static/admin/css
RUN mkdir -p /app/static/admin/js
RUN mkdir -p /app/static/rest_framework/img
RUN mkdir -p /app/static/rest_framework/css
RUN mkdir -p /app/static/rest_framework/js
RUN mkdir -p /app/static/rest_framework/fonts
RUN mkdir -p /app/static/rest_framework/docs
#RUN apt-get update && apt-get install -y acl
#RUN setfacl -R -m u:unit:rwx /app
#RUN setfacl -R -m d:u:unit:rwx /app
#RUN chown -R unit:unit /app && chmod -R 770 /app


RUN useradd --no-create-home --shell /bin/false user
RUN chown -R user:user /app/static
RUN chmod -R 777 app/static

#RUN mkdir -p app/static/
#RUN chown -R unit:unit ./

# Команда для сбора статических файлов Django
#RUN python app/manage.py collectstatic --noinput
WORKDIR /app
#RUN mkdir -p /vol/web/static/
RUN ls -lah
# Удаление файла конфигурации по умолчанию и копирование нашей конфигурации
RUN rm -f /docker-entrypoint.d/*.json
COPY /unit.config.json /docker-entrypoint.d/config.json
#RUN chown -R unit:unit /app

#RUN chown -R unit:unit app/static/
# Определяем порт, который будет прослушивать приложение
EXPOSE 8300
USER user
#CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]