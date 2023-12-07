# Описание общих API интерфейсов проекта

## Общая информация

API версионируется префиксом в пути URL для обратной совместимости
клиентских приложений. Например: `api/v1/product-list/` 

Общий формат обмена данными (ответ) в формате JSON:

```javascript
{
    code: int
    msg: string
    data: {}
}
```

## Пагинация

Интерфейсы dealer-product-list () и product-to-matched-list () могут быть параметризированными:

* `offset` - (int) смещение курсора списка.
* `limit` - (int) количество в ответе.

## Описание интерфейсов

### Cписок товаров производителя

GET `api/{v1}/product-list/`

```javascript
{
    products_count : int
    products : [
        {
            id : int
            article : string
            ean_13 : string
            name : string
            cost : float
            min_rec_price  : float
            rec_price : float
            category_id : float
            ozon_name : string 
            name_1c : string
            ozon_article : string
            wb_article : string
            ym_article : string
        }
    ]
}
```

### Cписок не размеченных товаров

GET `api/{v1}/product-to-matched-list/`

```javascript
{
    dealer_products_count : int
    offset : int
    limit : int
    dealer_products : [
        dealer_product : 
            {
                id : int
                dealer : {
                    id : int
                    name : string
                }
                price : string
                date : datetime
                product_url : string
                product_name  : string
                dealer_product_status : [
                    {
                        status : string
                        status_datetime : datetime
                    }
                ]
                dealer_product_history : [
                    {
                        status_type : string
                        status_datetime : datetime
                    }
                ]
            }
        procreator_variants : [
            {
                id: int
                name_1c : string
            }
        ]
    ]
}
```

### Cписок товаров диллеров

GET `api/{v1}/dealer-product-list/`

```javascript
{
    products_count : int
    offset : int
    limit : int
    product_list : [
        dealer_product : 
            {
                procreator_product : {
                    id : int
                    article : string
                    ean_13 : string
                    name : string
                    cost : float
                    min_rec_price  : float
                    rec_price : float
                    category_id : float
                    ozon_name : string 
                    name_1c : string
                    ozon_article : string
                    wb_article : string
                    ym_article : string
                }
                dealer_product_info : {
                    id : int
                    dealer : {
                        id : int
                        name : string
                    }
                    price : string
                    date : datetime
                    product_url : string
                    product_name  : string
                    dealer_product_status : [
                        {
                            status : string
                            status_datetime : datetime
                        }
                    ]
                    dealer_product_history : [
                        {
                            status_type : string
                            status_datetime : datetime
                        }
                    ]
                }
            }
        procreator_variants : [
            {
                id: int
                name_1c : string
            }
        ]
    ]
}
```

### Метод сопоставления товара образцу (действие разметки)

POST `api/{v1}/product-matching/`

* `button` - (string) принимает значения approve|aside|disapprove.
* `dealer_product_id` - (int) id товара диллера.
* `product_id` - (int) id товара производителя.
* `is_manual` - (string) признак выбора вручную, принимает значения True|False.

При успешном результате отправляет `Ok` в ключе `msg`.

### Cписок диллеров

GET `api/{v1}/dealer-list/`

```javascript
{
    dealers_count : int
    dealers : [
        {
            id : int
            name : string
        }
    ]
}
```

### Cписок товаров диллера

GET `api/{v1}/dealer-list/`

```javascript
{
    dealers_count : int
    dealer : {
        id : int
        name : string
    }
    dealer_products : [
        {
            product : {
                id : int
                article : string
                ean_13 : string
                name : string
                cost : float
                min_rec_price  : float
                rec_price : float
                category_id : float
                ozon_name : string 
                name_1c : string
                ozon_article : string
                wb_article : string
                ym_article : string
            }
            dealer_product_info : {
                id : int
                dealer : {
                    id : int
                    name : string
                }
                price : string
                date : datetime
                product_url : string
                product_name  : string
                dealer_product_status : [
                    {
                        status : string
                        status_datetime : datetime
                    }
                ]
                dealer_product_history : [
                    {
                        status_type : string
                        status_datetime : datetime
                    }
                ]
            }
        }
    ]
}
```

### Принудительное обновление рекомендаций

POST `api/{v1}/ml-force-update/`

При успешном запуске обновления отправляет `Ok` в ключе `msg`.

### Принудительное обновление рекомендаций

POST `api/{v1}/ml-force-update-product/`

При успешном запуске обновления отправляет `Ok` в ключе `msg`.

### Справочники приложения

GET `api/{v1}/references/`

Отдает два списка ключ:знгачение ключей используемых в API проекта

```javascript
{
    conditions : [
        {}
    ]
    status_types : [
        {}
    ]
}
```
