# Описание генератора первичной истории и статусов продуктов диллера

Генератор используется для наполнения моделей `Изменение статуса` и `История статусов` данных предоставленных заказчиком в csv файлах.

Реализован в качестве функции Python.

Результат работы генератора выводится в лог (консоль).

Запуск генератора осуществляется при включенном виртуальном окружении после успешной отработки парсера данных:

```shell
python путь_до_репозитория/backend/manage.py change_status
```
