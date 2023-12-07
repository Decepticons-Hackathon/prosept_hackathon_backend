## Общие требования

* Docker >= ____

Рекомендуется где-то создать папку проекта, например `/home/username/prosept` далее:

```shell
mkdir /home/username/prosept
cd $_
git clone git@github.com:Decepticons-Hackathon/prosept_hackathon_backend.git
```

### Запуск в контейнерах Docker
```
cd infra/
```

```
docker-compose up -d --build
```

Для запуска генератора вариантов матчинга товаров диллеров необходимо установить расписание запуска генератора (пример для crontab - каждые 15 минут):
```shell
*/15 * * * * root docker exec python путь_до_репозитория/backend/manage.py get_recomendations --v 2
```

Приложение доступно по адресу `http://127.0.0.1:8080/`.
