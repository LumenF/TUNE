from django.contrib import admin

from apps.abstraction.admin import AbstractAdmin
from apps.apps.configs.geography.models import CityModel, InviteModel, SuppProviderModel


@admin.register(CityModel)
class CityAdmin(AbstractAdmin):
    list_display = (
        'name',
        'id',
    )

    search_fields = (
        'name',
    )


@admin.register(InviteModel)
class InviteAdmin(AbstractAdmin):
    list_display = (
        'name',
        'count',
    )


@admin.register(SuppProviderModel)
class SuppProviderAdmin(AbstractAdmin):
    list_display = (
        'name',
        'SITE_ID',
        'id',
    )
    search_fields = (
        'name',
    )
