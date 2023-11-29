from django.db import models


class Dealer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)


class Product(models.Model):
    product_id = models.IntegerField()
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
