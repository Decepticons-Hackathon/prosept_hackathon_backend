# Описание API интерфейсов проекта (аналитика)

### Статистика по диллерам

GET `api/{v1}/dealers-stat/`

```javascript
{
    dealers : [
        {
            dealer : {
                id : int
                name : string
            }
            stat_all : {
                approve: int
                disapprove: int
                aside: int
                none: int
            }
            stat_today : {
                approve: int
                disapprove: int
                aside: int
                none: int
            }
        }
    ]
}
```

### Статистика обработки моделью ДС

GET `api/{v1}/match-stat/`

```javascript
{
    ds : int
    manual : int
    cancel : int
    var_1 : int
    var_2 : int
    var_3 : int
    var_4 : int
    var_5 : int
}
```

### Информация о товарах диллера

GET `api/{v1}/dealer-detail/{id}/`

```javascript
{
    dealer_products_count : int
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

### Информация о товаре диллера (только при наличии истории)

GET `api/{v1}/product-stat/{id}/`

```javascript
{
    dealer_product : {
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
```
