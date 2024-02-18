#FROM nginx/unit:1.26.1-python3.9
#FROM unit:1.31.1-python3.11
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN adduser -D user
USER user
# Add NGINX's official signing key
RUN apt-get update && apt-get install -y gnupg && \
    curl --output /usr/share/keyrings/nginx-keyring.gpg https://unit.nginx.org/keys/nginx-keyring.gpg

# Configure the NGINX Unit repository for Debian
RUN echo "deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ bullseye unit" > /etc/apt/sources.list.d/unit.list && \
    echo "deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ bullseye unit" >> /etc/apt/sources.list.d/unit.list

# Install NGINX Unit and the Python 3.11 module
RUN apt-get update && \
    apt-get install -y unit unit-python3.11


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


RUN adduser -D user
RUN chown -R user:user /app/static
RUN chmod -R 777 /app/static



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

# Expose default NGINX Unit port
EXPOSE 8300

# Start NGINX Unit
CMD ["unitd", "--no-daemon"]
#CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]