#!/bin/bash

# Запуск NGINX Unit
unitd --no-daemon --control unix:/var/run/control.unit.sock &

# Ожидание готовности управляющего сокета
while [ ! -S /var/run/control.unit.sock ]; do
    sleep 1
done

# Применение конфигурации
curl -X PUT --data-binary @/docker-entrypoint.d/config.json --unix-socket /var/run/control.unit.sock http://localhost/config/

# Поддержание работы контейнера
wait