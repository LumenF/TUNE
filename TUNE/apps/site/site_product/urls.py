from django.template.defaulttags import url
from django.urls import path, re_path

from apps.site.index.views import IndexView
from apps.site.site_product.views import CategoryView

urlpatterns = [
    path('<str:category>', CategoryView.as_view(), name='catalog'),

]
