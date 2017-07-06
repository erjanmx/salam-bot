[![Build Status](https://travis-ci.org/erjanmx/salam-bot.svg?branch=master)](https://travis-ci.org/erjanmx/salam-bot)

# Салам бот

Бот для мессенджера [NambaOne](https://namba1.co/) победивший в конкурсе 'BattleBot' устроенной создателями мессенджера

Позволяет связать двоих случайных пользователей в один чат позволяя им общаться между собой не раскрывая свои настоящие личности

#### Демонстрация
![Imgur](http://i.imgur.com/rNPY46j.gif)

## Установка

Приложение работает на [Flask](http://flask.pocoo.org/), в качестве работы с БД используется [orator](https://orator-orm.com/)

### Зависимости

- python3 с pip и virtualenv
- mysql

### Создание и активация virtualenv

```bash
virtualenv venv
source venv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск

Приложение настраивается через `.env` файл или указав значения в переменных окружения
```
cp .env.example .env
```

После задания настроек необходимо запустить команду миграции для создания необходимых таблиц, предварительно создав базу данных

```
orator migrate -c config/settings.py -p database/migrations/ -f
```

Если миграции выполнились успешно то можно уже запустить командой

```bash
python app.py
```

### Закрытие неактивных чатов

Если после создания чата собеседник не ответил в течение трех минут то чат должен быть закрыт с уведомлением обоих сторон

Для этого необходимо поставить вызов по расписанию endpoint-a приложения с соответствующими параметрами, а именно

```
curl -X POST \
  'url' \
  -H 'content-type: application/json' \
  -d '{"event":"cron/close_idle_chats","data":""}'
```
