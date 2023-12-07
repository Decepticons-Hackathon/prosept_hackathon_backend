from django.urls import include, path, re_path
from django.conf import settings
from api.management.schema import schema_view
from api.views import v1

url_list = [
    path('product-to-matched-list/', v1.ProductListToMatches.as_view(), name='product_to_matched_list'),
    path('product-list/', v1.ProductList.as_view(), name='product_list'),
    path('dealer-product-list/', v1.DealerProductList.as_view(), name='dealer_product_list'),
    path('product-matching/', v1.ProductMatching.as_view(), name='product_matching'),
    path('dealer-list/', v1.DealerList.as_view(), name='dealer_list'),
    path('dealers-stat/', v1.DealersStat.as_view(), name='dealers_stat'),
    path('match-stat/', v1.MLStat.as_view(), name='ml_stat'),
    re_path(r'dealer-detail/(?P<pk>\w+)/$', v1.DealerDetail.as_view(), name='dealer_detail'),
    re_path(r'product-stat/(?P<pk>\w+)/$', v1.ProductsStat.as_view(), name='product_stat'),
    path('ml-force-update/', v1.MlForceUpdate.as_view(), name='ml_force_update'),
    path('ml-force-update-product/', v1.MlForceUpdateProduct.as_view(), name='ml_force_product_update'),
    path('references/', v1.AppDicts.as_view(), name='references'),
]

urlpatterns = [
    path('v1/', include(url_list),)
]

if settings.DEBUG:
    url_list += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
