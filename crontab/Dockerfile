FROM python:3.9

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y cron && apt install vim -y

# Копирование скрипта в контейнер
COPY script.sh /script.sh

RUN chmod +x /script.sh

# Установка cron
RUN apt-get install -y cron

# Добавление задания в cron
RUN echo "59 20 * * * root /script.sh" > /etc/cron.d/cron
RUN #echo "* 19 * * * root /script.sh" > /etc/cron.d/cron_1

# Запуск cron при старте контейнера
CMD cron && tail -f /dev/null



