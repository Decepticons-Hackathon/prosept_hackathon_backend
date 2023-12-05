from django.db import models


class Dealer(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64, db_index=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    product_id = models.PositiveIntegerField(db_index=True)
    article = models.CharField(
        max_length=64
    )
    ean_13 = models.CharField(
        max_length=64
    )
    name = models.CharField(
        max_length=256,
        db_index=True
    )
    cost = models.FloatField()
    min_rec_price = models.FloatField(
        null=True,
        blank=True
    )
    rec_price = models.FloatField()
    category_id = models.FloatField()
    ozon_name = models.CharField(
        max_length=256,
    )
    name_1c = models.CharField(
        max_length=256,
        db_index=True
    )
    wb_name = models.CharField(
        max_length=256
    )
    ozon_article = models.CharField(
        max_length=64
    )
    wb_article = models.CharField(
        max_length=64
    )
    ym_article = models.CharField(
        max_length=64
    )

    def __str__(self) -> str:
        return f'{self.name}'


class DealerPrice(models.Model):
    product_key = models.CharField(
        max_length=256,
        db_index=True
    )
    price = models.FloatField()
    product_url = models.CharField(
        max_length=256
    )
    product_name = models.CharField(
        max_length=64,
        db_index=True
    )
    date = models.DateField()
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.product_key}'


class DealerProduct(models.Model):
    key = models.ManyToManyField(
        DealerPrice
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    dealer_id = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE
    )


class DealerProductVariants(models.Model):
    dealer_product_id = models.ForeignKey(
        DealerPrice,
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    dealer_id = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE
    )
    degree_of_agreement = models.IntegerField()


CORRECT_CONDITIONS = (
    ('approve', 'Подтвердить',),
    ('disapprove', 'Отклонить',),
    ('aside', 'Отложить',),
    ('none', 'Не определено',),
)


class DealerProductStausChange(models.Model):
    dealer_product_id = models.ForeignKey(
        DealerPrice,
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    dealer_id = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=CORRECT_CONDITIONS,
        default=CORRECT_CONDITIONS[3][0],
        db_index=True
    )
    status_datetime = models.DateTimeField(
        auto_now_add=True
    )


STATUS_TYPE = (
    ('ds', 'Рекомендательная модель',),
    ('manual', 'Поиск в ручную',),
    ('none', 'Не размечен',),
    ('aside', 'Отложенный',),
    ('cancel', 'Сброшенный',),
)


class DealerProductStausHistory(models.Model):
    dealer_product_id = models.ForeignKey(
        DealerPrice,
        on_delete=models.CASCADE
    )
    status_datetime = models.DateTimeField(
        auto_now_add=True
    )
    status_type = models.CharField(
        max_length=6,
        choices=STATUS_TYPE,
        default=STATUS_TYPE[2][0],
        db_index=True
    )
    product_variant = models.ForeignKey(
        DealerProductVariants,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
