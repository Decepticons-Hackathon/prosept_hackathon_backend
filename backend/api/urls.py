from django.urls import include, path, re_path

from api import views
from api.management.schema import schema_view

url_list = [
    path('product-to-matched-list/', views.ProductListToMatches.as_view(), name='product_to_matched_list'),
    path('product-list/', views.ProductList.as_view(), name='product_list'),
    path('dealer-product-list/', views.DealerProductList.as_view(), name='dealer_product_list'),
    path('product-matching/', views.ProductMatching.as_view(), name='product_matching'),
    path('dealer-list/', views.DealerList.as_view(), name='dealer_list'),
    re_path(r'dealer-detail/(?P<pk>\w+)/$', views.DealerDetail.as_view(), name='dealer_detail'),
    re_path(r'product-stat/(?P<pk>\w+)/$', views.ProductsStat.as_view(), name='product_stat'),
    path('ml-force-update/', views.MlForceUpdate.as_view(), name='ml_force_update'),
    # TODO: Перенести в backend, сделать зависимым от debug=True
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = [
    path('v1/', include(url_list),)
]
