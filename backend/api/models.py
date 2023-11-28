from django.db import models


class Dealer(models.Model):
    name = models.CharField(
        max_length=64
    )


class Product(models.Model):
    article = models.CharField(
        max_length=64
    )
    ean_13 = models.CharField(
        max_length=64
    )
    name = models.CharField(
        max_length=64
    )
    cost = models.PositiveIntegerField()
    min_rec_price = models.PositiveIntegerField()
    rec_price = models.PositiveIntegerField()
    category_id = models.PositiveIntegerField()
    ozon_name = models.CharField(
        max_length=64,
    )
    name_1c = models.CharField(
        max_length=64,
    )
    wb_name = models.CharField(
        max_length=64
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


class DealerPrice(models.Model):
    product_key = models.PositiveIntegerField(
        primary_key=True
    )
    price = models.PositiveIntegerField()
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


class DealerProduct(models.Model):
    key = models.ForeignKey(
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
