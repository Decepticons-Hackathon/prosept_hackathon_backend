# prosept_hackathon_backend

# Разработка серверной части

## Общие требования

* Python = 3.10
* Django >= 4.2

## Для nix-подобных систем

Рекомендуется где-то создать папку проекта, например `/home/username/prosept` далее:

```shell
mkdir /home/username/prosept
cd $_
git clone git@github.com:Decepticons-Hackathon/prosept_hackathon_backend.git
mkdir data
```

### Подготовка среды выполнения

Для запуска сервера разработки следует установить Python 3.10, пакетный менеджер PIP и менеджер виртуального окружения. Пример для Ubuntu: 

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt -y install python3.10 python3.10-distutils python3.10-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.10 get-pip.py
python3.11 -m pip install virtualenv
```

Можно добавить файл настроек в `<каталог репозитория>/server/backend/local_settings.py`:

```python
_ROOT_PATH = '/home/username/prosept/data' # каталог где будет лежать файл базы и файлы таблиц csv

DEBUG = True

SECRET_KEY = 'xxx'

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{_ROOT_PATH}/prosept.db',
    }
}

MEDIA_ROOT = f'{_ROOT_PATH}/media'

AUTH_PASSWORD_VALIDATORS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'handlers': {
        'trace': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{_ROOT_PATH}/prosept.server.log',
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'handlers': ['trace', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
```

### Первый запуск

При **первом** запуске локального сервера разработки следует выполнить:

```shell
cd /путь_указанный_в_переменной_ROOT_PATH
python3.10 -m virtualenv -p python3.10 env
. ./env/bin/activate
pip install -r путь_до_репозитория/server/requirements.txt
python путь_до_репозитория/server/manage.py migrate
python путь_до_репозитория/server/manage.py loaddata preload_data.json
python путь_до_репозитория/server/manage.py runserver 8080
```

Приложение доступно по адресу `http://127.0.0.1:8080/`.

### Все последующие запуски

```shell
cd /путь_указанный_в_переменной_ROOT_PATH
. ./env/bin/activate
python путь_до_репозитория/server/manage.py runserver 8080
```

### Запуск в контейнерах Docker
```
cd infra/
```

```
docker-compose up -d --build
```

Приложение доступно по адресу `http://127.0.0.1:8080/`.
