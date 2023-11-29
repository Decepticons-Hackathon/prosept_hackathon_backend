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


class DealerProductSerializer(serializers.Serializer):
    # dealer = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    def _get_dealer_prices(self, obj):
        dealer_prices = []
        for price in DealerPriceSerializer(obj.key, many=True).data:
            dealer_prices.append(DealerPriceSerializer(price).data)
        return dealer_prices

    # def get_dealer(self, obj):
    #     return DealerSerializer(obj.dealer_id).data

    def get_product(self, obj):
        data = ProductSerializer(obj.product_id).data
        data['dealer_prices'] = self._get_dealer_prices(obj)
        return data
