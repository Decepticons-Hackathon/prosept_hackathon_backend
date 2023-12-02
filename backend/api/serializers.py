from rest_framework import serializers

# from api.models import Dealer, Product, DealerPrice, DealerProduct


class DealerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=64)


class ProductSerializer(serializers.Serializer):
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


class DealerPriceSerializer(serializers.Serializer):
    price = serializers.FloatField()
    date = serializers.DateField()
    product_url = serializers.CharField(max_length=256)
    product_name = serializers.CharField(max_length=64)


class DealerProductSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        data = ProductSerializer(obj.product_id).data
        data["dealer_prices"] = DealerPriceSerializer(obj.key, many=True).data
        return data


class DealerDetailSerializer(serializers.Serializer):
    dealer = DealerSerializer()
    dealer_products = DealerProductSerializer(many=True)
    dealer_products_count = serializers.SerializerMethodField()

    def get_dealer_products_count(self, obj):
        return len(obj.dealer_products)
