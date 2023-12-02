from django.db import models


class Dealer(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    product_id = models.PositiveIntegerField()
    article = models.CharField(
        max_length=64
    )
    ean_13 = models.CharField(
        max_length=64
    )
    name = models.CharField(
        max_length=256
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
        max_length=256
    )
    price = models.FloatField()
    product_url = models.CharField(
        max_length=256
    )
    product_name = models.CharField(
        max_length=64
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


# Проработка моделей для маппинга


class DealerProductVariants(models.Model):
    dealer_product_id = models.ForeignKey(
        DealerProduct,
        on_delete=models.CASCADE
    )
    product_id = models.ManyToManyField(
        Product
    )
    dealer_id = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE
    )


class DealerProductMapped(models.Model):
    dealer_product_id = models.ForeignKey(
        DealerProduct,
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


CORRECT_CONDITIONS = (
    ('true', 'Подтвердить',),
    ('false', 'Отклонить',),
    ('none', 'Отложить',),
)


class DealerProductStausChange(models.Model):
    dealer_product_id = models.ForeignKey(
        DealerProduct,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=5,
        choices=CORRECT_CONDITIONS,
        null=True, blank=True,
    )
    status_datetime = models.DateTimeField(
        auto_now_add=True
    )
