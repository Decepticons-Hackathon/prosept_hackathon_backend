from rest_framework import serializers

# from api.models import Dealer, Product, DealerPrice, DealerProduct


class DealerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=64)

class ProductListSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    article = serializers.CharField(max_length=64)
    ean_13 = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=256)
    cost = serializers.FloatField()
    min_rec_price = serializers.FloatField(required=None)
    rec_price = serializers.FloatField()
    category_id = serializers.FloatField()
    ozon_name = serializers.CharField(max_length=256)
    name_1c = serializers.CharField(max_length=256)
    wb_name = serializers.CharField(max_length=256)
    ozon_article = serializers.CharField(max_length=64)
    wb_article = serializers.CharField(max_length=64)
    ym_article = serializers.CharField(max_length=64)
