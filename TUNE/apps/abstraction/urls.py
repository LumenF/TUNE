from django.urls import path

from apps.abstraction.views import report

urlpatterns = [
    # path('', StatisticView.as_view()),
    # path('index', StatisticView.as_view()),
    path('', report),
]
