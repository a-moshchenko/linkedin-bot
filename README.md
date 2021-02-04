# LinkedIn-bot

*Проверялся на версии python 3.7.5*

Устанавливаем pyenv
`https://khashtamov.com/ru/pyenv-python/`

Устанавливаем python 3.7.5

`pyenv install 3.7.5`

Переключаемся на версию python3.7.5
`pyenv local 3.7.5`

Далее комманды по порядку
`python -m pip install virtualenv`

`python -m venv env`

`. env/bin/activate`

`pip install -r requirements.txt`

Создаем БД
`python database/database.py`

***В файле config.py меняем значение DEBUG на False***
***в режиме DEBUG соообщения не отправляются и браузер работает без --headless***

Запуск Бота
`python main.py`

Для выгрузки контактов у которых есть email:
`python get_csv.py`
