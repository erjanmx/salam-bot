# Salam Bot

## Установка

Необходим `python3`, `pip` и `virtualenv`

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
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
