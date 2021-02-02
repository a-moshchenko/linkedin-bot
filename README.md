1 Копируем репозиторий
git clone https://github.com/dedicated-rpa/linkedin-bot.git
переходим в ветку fix_by_dev5044

2 В файле config.py меняем значение DEBUG на False
(при значении True сообщение не отправляется, а закрывается окно. И драйвер без режима headless)

3 Устанавливаем зависимости  pip3 install -r requirements.txt

4 Запускаем бота  python3 main.py

5 ищем бота в Телеграмм ('@dev_5044_test_bot')

6 Бот собирает email если есть, можно выгрузить в csv коммандой python3 get_csv.py

Обязательно при первом запуске не пропускаем пункт изменить сообщение
