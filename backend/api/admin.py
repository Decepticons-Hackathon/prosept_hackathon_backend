from django.contrib import admin

from api.models import (
    Dealer,
    DealerPrice,
    DealerProduct,
    DealerProductMapped,
    DealerProductStausChange,
    DealerProductVariants,
    Product,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("name", "product_id", "article", "ean_13")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("name", "id")


@admin.register(DealerPrice)
class DealerPriceAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("product_name", "product_key", "id")


@admin.register(DealerProduct)
class DealerProductAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("product_id", "dealer_id")


@admin.register(DealerProductVariants)
class DealerProductVariantsAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("dealer_product_id", "dealer_id")


@admin.register(DealerProductMapped)
class DealerProductMappedAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("dealer_product_id", "product_id", "dealer_id")


@admin.register(DealerProductStausChange)
class DealerProductStausChangeAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("dealer_product_id", "status", "status_datetime")
