from django.urls import path

from apps.apps.user.views import user_active

urlpatterns = [
    path('<str:year>/<str:month>', user_active, name='user_active'),
]
