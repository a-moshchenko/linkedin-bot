# linkedin-bot
Linkedin bot

* Используем Sales Navigator
* Задаем фильтры
* Ищем людей, профиль которых открыт и делаем connect + отправку сообщения
* Вносим человека, которому отправляли, чтоб не слать это дважды
* Управляем через телеграмм:
* 1. Заливая список компаний в файле
* 2. Просто настраивая фильтр для sales навигатор

# Deployment

Просто триггернуть ветку deployment (empty commit).
В ветке указан пример для команд которые синкают код и запускают версию питона
Заменить на скрипт для (ре)старта бота


# ИНСТРУКЦИЯ ДЕПЛОЯ НА СЕРВЕР ПО SSH
ВСЕ КОМАНДЫ ВВОДЯТСЯ С РУТ ДОСТУПОМ

"sudo apt update" - обновляем файлы на сервере, для избегания лишних ошибок

"apt-get install supervisor -y" - устанавливаем программу supervisor в которой будет создана программа бота. Ее мы будем запускать.

Создаем в папке с файлами бота, еще один файл bot.conf

******файл bot.conf******

[program:telegrambot]
directory=/home/ubuntu/telegrambot
command=python3 main.py

autostart=true
autorestart=true
environment=HOME="/home/ubuntu",USER="ваш юзер сервера"

stderr_logfile=/home/ubuntu/telegrambot/logfile_err.log
stdout_logfile=/home/ubuntu/telegrambot/logfile.log

******файл bot.conf конец******

В файловой системе создаем в папке home, папку ubuntu, в ней папку telegrambot

грузим файлы бота в папку telegrambot

"apt install python3-pip" - установка pip
"python3 -m pip install -r requirements.txt -y" - установка библиотек из requirements.txt

"cp bot.conf /etc/supervisor/conf.d/bot.conf" - копируем bot.conf в папку supervisor
"supervisorctl reread" - считываем файл
"supervisorctl update" - программа запускается

----------- для просмотра лога ошибок--------
"supervisorctl"
"tail -f telegrambot stderr"

----------управление программой---------
start telegrambot - запуск
stop telegrambot - стоп
restart telegrambot - перезапуск


---------‐установка chrome----------
Скачваем Chrome:

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
И сразу же устанавливаем:

sudo dpkg -i google-chrome-stable_current_amd64.deb
