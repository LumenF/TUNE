from django.urls import path

from apps.apps.product.views import product_static, summ_product_static, category_static

urlpatterns = [
    path('summ/<str:year>/<str:month>', summ_product_static, name='summ_product_static'),
    path('category/<str:year>/<str:month>', category_static, name='category_views'),
    path('<str:year>/<str:month>/<str:category_id>', product_static, name='product_static'),
]
