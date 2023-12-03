from rest_framework import serializers


class ProductMlSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=256)
    category_id = serializers.FloatField()


class DealerProductMlSerializer(serializers.Serializer):
    dealer_product_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    dealer_id = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.dealer_product_id.product_name

    def get_dealer_id(self, obj):
        return obj.dealer_id.id

    def get_dealer_product_id(self, obj):
        return obj.dealer_product_id.id
