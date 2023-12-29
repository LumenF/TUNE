import json
import pickle

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from TUNE.settings import s_redis_user
from apps.abstraction.admin import AbstractAdmin
from apps.apps.user.models import UserModel, TgUserModel


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'city',
        'report',
        'notice'
    )
    autocomplete_fields = (
        'city',
    )
    fieldsets = (
        (_('Personal info'), {
            'fields': (
                'username',
                'password',
                'first_name',
                'last_name',
                'email',
                'city',
            )
        }
         ),

        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                ),
            },
        ),

    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'password1',
                    'password2',
                    'city',
                ),
            },
        ),
    )


@admin.register(TgUserModel)
class TgUserAdmin(AbstractAdmin):
    list_display = (
        '__str__',
        'city',
        'phone',
        'is_blocked_bot',
        'is_ban_user',
        'last_login',
        'date_created',
        'id'
    )
    search_fields = (
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'phone',
    )
    list_filter = (
        'city',
        'is_blocked_bot',
        'is_ban_user',
        'is_staff',
        'segment',
    )

    actions = (
        'ban_user',
        'unban_user',
        'add_admin',
        'remove_admin',
    )
    autocomplete_fields = (
        'city',
    )
    fields = (
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'phone',
        'city',
        'segment',
        'is_blocked_bot',
        'is_ban_user',
        'is_staff',
        'notice',
    )

    @admin.action(description='Забанить пользователя')
    def ban_user(self, request, queryset):
        queryset.update(is_ban_user=True)

        for user in queryset:
            user: TgUserModel
            check = s_redis_user.get(user.tg_id)
            if not check:
                p_mydict = json.dumps({'ban': user.is_ban_user, 'staff': user.is_staff})
                s_redis_user.set(user.tg_id, p_mydict)
        self.message_user(
            request=request,
            message='Успешно забанен',
            level=messages.INFO
        )

    @admin.action(description='Разбанить пользователя')
    def unban_user(self, request, queryset):
        queryset.update(is_ban_user=False)
        for user in queryset:
            user: TgUserModel
            check = s_redis_user.get(user.tg_id)
            if not check:
                p_mydict = json.dumps({'ban': user.is_ban_user, 'staff': user.is_staff})
                s_redis_user.set(user.tg_id, p_mydict)
            else:
                s_redis_user.delete(user.tg_id)
                p_mydict = json.dumps({'ban': user.is_ban_user, 'staff': user.is_staff})
                s_redis_user.set(user.tg_id, p_mydict)
        self.message_user(
            request=request,
            message='Успешно снят бан',
            level=messages.INFO
        )

    @admin.action(description='Дать админ-права')
    def add_admin(self, request, queryset):
        queryset.update(is_staff=True)

        self.message_user(
            request=request,
            message='Права успешно выданы',
            level=messages.WARNING
        )

    @admin.action(description='Забрать админ-права')
    def remove_admin(self, request, queryset):
        queryset.update(is_staff=False)
        self.message_user(
            request=request,
            message='Права успешно отозваны',
            level=messages.INFO
        )
