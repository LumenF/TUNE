from django.urls import path

from apps.apps.configs.parameter.views import show_csv, show_csv_only_amount

urlpatterns = [
    path('show/<int:pk>', show_csv),
    path('show/only_amount/<int:pk>', show_csv_only_amount),

]