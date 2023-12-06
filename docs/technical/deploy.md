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

Приложение доступно по адресу `http://127.0.0.1:8080/`.
