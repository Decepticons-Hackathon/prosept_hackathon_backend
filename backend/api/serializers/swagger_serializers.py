from rest_framework import serializers

from api.models import Dealer, DealerPrice, DealerProduct, Product

# -------------------- Base --------------------


class SwaggerDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'


class SwaggerProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class SwaggerDealerProductStatus(serializers.ModelSerializer):
    status = serializers.CharField()
    status_datetime = serializers.DateTimeField()

    class Meta:
        model = Dealer
        fields = ('status', 'status_datetime')


class SwaggerDealerProductHistory(serializers.ModelSerializer):
    status_type = serializers.CharField()
    status_datetime = serializers.DateTimeField()

    class Meta:
        model = Dealer
        fields = ('status_type', 'status_datetime')


class SwaggerDealerPriceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    dealer = SwaggerDealerSerializer()
    price = serializers.FloatField()
    date = serializers.DateField()
    product_url = serializers.CharField(max_length=256)
    product_name = serializers.CharField(max_length=256)
    dealer_product_status = SwaggerDealerProductStatus()
    dealer_product_history = SwaggerDealerProductHistory()

# -------------------- In-between --------------------


class SwaggerProductsForDealer(serializers.ModelSerializer):
    procreator_product = SwaggerProductSerializer()
    dealer_product_info = SwaggerDealerPriceSerializer()

    class Meta:
        model = Product
        fields = ['procreator_product', 'dealer_product_info']


class SwaggerProcreatorVariants(serializers.Serializer):
    id = serializers.IntegerField()
    name_1c = serializers.CharField()

    class Meta:
        fields = ('id', 'name_1c')


class SwaggerStat(serializers.Serializer):
    approve = serializers.IntegerField()
    disapprove = serializers.IntegerField()
    aside = serializers.IntegerField()
    none = serializers.IntegerField()

    class Meta:
        model = DealerPrice
        fields = ['approve', 'disapprove', 'aside', 'none']


class SwaggerDealerStat(serializers.Serializer):

    dealer = SwaggerDealerSerializer()
    stat_all = SwaggerStat()
    stat_today = SwaggerStat()

    class Meta:
        fields = ['dealer', 'stat_all', 'stat_today']


class SwaggerDealerProduct(serializers.Serializer):
    dealer_product = SwaggerProductsForDealer()
    procreator_variants = SwaggerProcreatorVariants()

    class Meta:
        fields = ('dealer_product', 'procreator_variants')


class SwaggerDealerProducts(serializers.Serializer):
    product = SwaggerProductSerializer()
    dealer_product_info = SwaggerDealerPriceSerializer()

    class Meta:
        fields = ['product', 'dealer_product_info']


class SwaggerDealerProductForMatch(serializers.Serializer):
    dealer_product = SwaggerDealerPriceSerializer()
    procreator_variants = SwaggerProcreatorVariants()

# -------------------- Final --------------------


class SwaggerProductMatch(serializers.Serializer):
    dealer_products = SwaggerDealerProductForMatch()
    offset = serializers.IntegerField()
    limit = serializers.IntegerField()
    dealer_products_count = serializers.IntegerField()

    class Meta:
        model = Dealer
        fields = ['dealer_products', 'offset', 'limit', 'dealer_products_count']


class SwaggerProductList(serializers.Serializer):
    products = SwaggerProductSerializer()

    class Meta:
        fields = ('products', )


class SwaggerDealerProductListSerializer(serializers.ModelSerializer):
    product_list = SwaggerDealerProduct()

    class Meta:
        model = DealerProduct
        fields = ['product_list',]


class SwaggerDealerDetailSerializer(serializers.ModelSerializer):
    dealer = SwaggerDealerSerializer()
    dealer_products = SwaggerDealerProducts()
    dealer_products_count = serializers.IntegerField()

    class Meta:
        model = Dealer
        fields = ['dealer', 'dealer_products', 'dealer_products_count']


class SwaggerDealersStatSerializer(serializers.Serializer):

    dealers = SwaggerDealerStat()

    class Meta:
        fields = ('dealers', )


class SwaggerMatchStatSerializer(serializers.Serializer):
    ds = serializers.IntegerField()
    manual = serializers.IntegerField()
    cancel = serializers.IntegerField()
    var_1 = serializers.IntegerField()
    var_2 = serializers.IntegerField()
    var_3 = serializers.IntegerField()
    var_4 = serializers.IntegerField()
    var_5 = serializers.IntegerField()

    class Meta:
        fields = ['ds', 'manual', 'cancel', 'var_1', 'var_2', 'var_3', 'var_4', 'var_5']
