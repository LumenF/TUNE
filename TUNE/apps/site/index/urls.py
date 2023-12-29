from django.template.defaulttags import url
from django.urls import path, re_path

from apps.site.index.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favorite/', IndexView.as_view(), name='favorite'),
    path('cart/', IndexView.as_view(), name='cart'),
    path('me/', IndexView.as_view(), name='me'),
]
