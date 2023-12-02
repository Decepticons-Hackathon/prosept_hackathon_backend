from rest_framework import serializers

from api.serializers.serializers import (
    DealerSerializer,
    DealerPriceSerializer,
    DealerProductSerializer,
    ProductListNotMatchesSerializer,
    ProductSerializer,
)


class ProductListResponseSerializer(serializers.Serializer):
    products = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    def get_products(self, obj):
        return ProductSerializer(obj, many=True).data

    def get_products_count(self, obj):
        return len(ProductSerializer(obj, many=True).data)


class ProductListToMatchesResponseSerializer(serializers.Serializer):
    dealer_products = serializers.SerializerMethodField()
    dealer_products_count = serializers.SerializerMethodField()

    def get_dealer_products(self, obj):
        return ProductListNotMatchesSerializer(obj, many=True).data

    def get_dealer_products_count(self, obj):
        return len(ProductListNotMatchesSerializer(obj, many=True).data)


class DealerListResponseSerializer(serializers.Serializer):
    dealers = serializers.SerializerMethodField()
    dealers_count = serializers.SerializerMethodField()

    def get_dealers(self, objects):
        return DealerSerializer(objects, many=True).data

    def get_dealers_count(self, objects):
        return len(DealerSerializer(objects, many=True).data)


class DealerDetailResponseSerializer(serializers.Serializer):
    dealer = serializers.SerializerMethodField()
    dealer_products = serializers.SerializerMethodField()
    dealer_products_count = serializers.SerializerMethodField()

    def get_dealer(self, objects):
        return DealerSerializer(objects[0].dealer_id).data

    def get_dealer_products(self, objects):
        return DealerProductSerializer(objects, many=True).data

    def get_dealer_products_count(self, objects):
        return len(DealerProductSerializer(objects, many=True).data)


class DealerProductStatResponseSerializer(serializers.Serializer):
    dealer_product = serializers.SerializerMethodField()

    def get_dealer_product(self, objects):
        return DealerPriceSerializer(objects[0].dealer_product_id).data
