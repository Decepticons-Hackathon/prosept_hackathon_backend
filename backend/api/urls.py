from django.urls import include, path, re_path

from api import views

url_list = [
    path('product-matched-list/', views.ProductListMatches.as_view(), name='product_matched_list'),
    path('product-list/', views.ProductList.as_view(), name='product_list'),
    re_path(r'^product-detail/(?P<pk>\w+)/$', views.ProductDetail.as_view(), name='product_detail'),
    path('dealer-list/', views.DealerList.as_view(), name='dealer_list'),
    re_path(r'dealer-detail/(?P<pk>\w+)/$', views.DealerDetail.as_view(), name='dealer_detail'),
    re_path(r'product-stat/(?P<pk>\w+)/$', views.ProductsStat.as_view(), name='product_stat'),
    re_path(r'operator-stat/(?P<pk>\w+)/$', views.OperatorStat.as_view(), name='operator_stat'),
]

urlpatterns = [
    path('v1/', include(url_list),)
]
