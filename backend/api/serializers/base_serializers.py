from rest_framework import serializers

from api.models import DealerProductStausChange, DealerProductStausHistory, DealerProductVariants


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


class ProductMiniSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name_1c = serializers.CharField(max_length=256)


class DealerPriceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    dealer = serializers.SerializerMethodField()
    price = serializers.FloatField()
    date = serializers.DateField()
    product_url = serializers.CharField(max_length=256)
    product_name = serializers.CharField(max_length=64)
    dealer_product_status = serializers.SerializerMethodField()
    dealer_product_history = serializers.SerializerMethodField()

    def get_dealer(self, obj):
        return DealerSerializer(obj.dealer).data

    def get_dealer_product_status(self, obj):
        obj_status = DealerProductStausChange.objects.get(
            dealer_product_id=obj.id
        )
        return DealerProductStatusSerializer(obj_status).data

    def get_dealer_product_history(self, obj):
        obj_status = DealerProductStausHistory.objects.filter(
            dealer_product_id=obj.id
        )
        return DealerProductHistorySerializer(obj_status, many=True).data


class DealerProductSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField()
    dealer_product_info = serializers.SerializerMethodField()

    def get_product(self, obj):
        return ProductSerializer(obj.product_id).data

    def get_dealer_product_info(self, obj):
        return DealerPriceSerializer(obj.key, many=True).data


class ProductListNotMatchesSerializer(serializers.Serializer):
    dealer_product = serializers.SerializerMethodField()
    procreator_variants = serializers.SerializerMethodField()

    def get_dealer_product(self, obj):
        return DealerPriceSerializer(obj.dealer_product_id).data

    def get_procreator_variants(self, obj):
        items = DealerProductVariants.objects.filter(
            dealer_product_id=obj.dealer_product_id
        ).order_by('degree_of_agreement')
        products_lst = []
        for item in items:
            products_lst.append(item.product_id)
        return ProductMiniSerializer(products_lst, many=True).data


class DealerProductStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=5)
    status_datetime = serializers.DateTimeField()


class DealerProductHistorySerializer(serializers.Serializer):
    status_type = serializers.CharField(max_length=6)
    status_datetime = serializers.DateTimeField()
