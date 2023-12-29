from datetime import datetime

from django.contrib import admin
from django.contrib import messages as level
from django.utils import timezone
from django.utils.safestring import mark_safe

from TUNE.settings import DEBUG
from apps.abstraction.admin import AbstractAdmin
from apps.apps.mailing.models import MailingAllModel, STATUS_SEND, MailingCityModel, SegmentBaseModel, \
    SegmentationStepModel, SegmentationModel, SegmentationReadyModel, MailingSegmentModel
from apps.apps.mailing.tasks import mail_all, mail_all_test, mail_city, mail_city_test, mail_segment_test, mail_segment, \
    mail_q_segment, mail_q_segment_test


class MailingBase(AbstractAdmin):

    @admin.action(description='Статус')
    def get_status(self, obj):
        anim = 'background-color: #f2f2f2; height: 20px; width: 0%; animation: fill-progress 2s ease-in-out infinite;'
        style_process = """<style>@keyframes fill-progress {0% { width: 0%;}100% {width: 100%;}}</style>"""
        style_error = """<style>@keyframes blink-text {0%{background-color: yellow;}50%{background-color: red;}100%{background-color: yellow;}}</style>"""
        for i in STATUS_SEND:
            if i[0] == obj.status:
                if i[0] == '0':
                    return mark_safe(f'<a style="background-color: #d4ffff;">{i[1]}</a>')
                if i[0] == '1':
                    return mark_safe(
                        f'{style_process}<div style="height: 20px;border-bottom: 5px solid #d4ffff; width: 50%;"><a style="display: block; height: 100%; border-bottom: 3px solid #5cff59; animation: fill-progress 2s ease-in-out infinite;">{i[1]}</a></div>')
                if i[0] == '2':
                    return mark_safe(f'<a style="border-bottom: 2px solid #5cff59;">{i[1]}</a>')
                if i[0] == '3':
                    return mark_safe(f'<a style="border-bottom: 2px solid red;">{i[1]}</a>')
                if i[0] == '4':
                    return mark_safe(
                        f'{style_error}<div style="height: 20px; width: 100%; background-color: #ff5d38;"><a style="display: block; height: 100%; background-color: yellow; animation: blink-text 1s ease-in-out infinite;">{i[1]}</a></div>')
                return mark_safe(f'<a style="border-bottom: 2px solid #85ffff;">{i[1]}</a>')
        return 'Ошибка'


@admin.register(MailingAllModel)
class MailingAllAdmin(MailingBase):
    list_display = (
        'name',
        'get_status',
        'get_counter',
        'redis_id',
        'date_send',
    )
    search_fields = (
        'name',
        'status',
    )
    list_filter = (
        'status',
    )
    actions = (
        'start_mailing',
        'start_mailing_test',
    )
    autocomplete_fields = (
        'products',
    )

    fields = [
        'name',
        'image_1',
        'text',
        'products',
        'status'
    ]
    readonly_fields = (
        'status',
    )
    if DEBUG:
        fields += [
            'count_success',
            'count_fail',
            'count_all',
            'redis_id'
        ]
        readonly_fields = ()

    @admin.action(description='Успешно/Ошибки/Всего')
    def get_counter(self, obj):
        return obj.get_counter()

    @admin.action(description='Запустить')
    def start_mailing(self, request, q):
        if len(q) != 1:
            return self.message_user(
                request=request,
                message='Вы можете запустить только 1 рассылку!',
                level=level.ERROR
            )
        q: MailingAllModel = q[0]
        if q.status != '0':
            return self.message_user(
                request=request,
                message='Вы можете запустить рассылку только со статусов "Не отправлено" !',
                level=level.ERROR
            )
        result = mail_all.delay(q.id)
        q.date_send = datetime.today()
        q.redis_id = result
        q.save()

    @admin.action(description='Запустить ТЕСТ')
    def start_mailing_test(self, request, q):
        if len(q) != 1:
            return self.message_user(
                request=request,
                message='Вы можете запустить только 1 рассылку!',
                level=level.ERROR
            )
        q: MailingAllModel = q[0]
        result = mail_all_test.delay(q.id)



@admin.register(MailingSegmentModel)
class MailingSegmentAdmin(MailingBase):
    list_display = (
        'name',
        'get_status',
        'get_counter',
        'redis_id',
        'date_send',
    )
    search_fields = (
        'name',
        'status',
    )
    list_filter = (
        'status',
    )
    actions = (
        'start_mailing',
        'start_mailing_test',
    )
    autocomplete_fields = (
        'products',
        'segment',
    )
    fields = [
        'name',
        'image_1',
        'text',
        'segment',
        'products',
        'status'
    ]
    readonly_fields = (
        'status',
    )
    if DEBUG:
        fields += [
            'count_success',
            'count_fail',
            'count_all',
            'redis_id'
        ]
        readonly_fields = ()

    @admin.action(description='Успешно/Ошибки/Всего')
    def get_counter(self, obj):
        return obj.get_counter()

    @admin.action(description='Запустить')
    def start_mailing(self, request, q):
        if len(q) != 1:
            return self.message_user(
                request=request,
                message='Вы можете запустить только 1 рассылку!',
                level=level.ERROR
            )
        q: MailingAllModel = q[0]
        if q.status != '0':
            return self.message_user(
                request=request,
                message='Вы можете запустить рассылку только со статусов "Не отправлено" !',
                level=level.ERROR
            )
        result = mail_segment(q.id)
        print(result)

    @admin.action(description='Запустить ТЕСТ')
    def start_mailing_test(self, request, q):
        if len(q) != 1:
            return self.message_user(
                request=request,
                message='Вы можете запустить только 1 рассылку!',
                level=level.ERROR
            )
        q: MailingAllModel = q[0]
        result = mail_segment_test(q.id)
        print(result)


@admin.register(MailingCityModel)
class MailingCityAdmin(MailingBase):
    list_display = (
        'name',
        'get_status',
        'get_counter',
        'city',
        'redis_id',
        'date_send',
    )
    search_fields = (
        'name',
        'status',
    )
    list_filter = (
        'status',
    )
    actions = (
        'start_mailing',
        'start_mailing_test',
    )
    autocomplete_fields = (
        'city',
        'products',
    )
    fields = [
        'name',
        'image_1',
        'text',
        'products',
        'city',
        'status'
    ]
    readonly_fields = (
        'status',
    )
    if DEBUG:
        fields += [
            'count_success',
            'count_fail',
            'count_all',
            'redis_id'
        ]
        readonly_fields = ()

    @admin.action(description='Успешно/Ошибки/Всего')
    def get_counter(self, obj):
        return obj.get_counter()

    @admin.action(description='Запустить')
    def start_mailing(self, request, q):
        if len(q) != 1:
            return self.message_user(
                request=request,
                message='Вы можете запустить только 1 рассылку!',
                level=level.ERROR
            )
        q: MailingAllModel = q[0]
        if q.status != '0':
            return self.message_user(
                request=request,
                message='Вы можете запустить рассылку только со статусов "Не отправлено" !',
                level=level.ERROR
            )
        result = mail_city.delay(q.id)
        print(result)
        q.redis_id = result
        q.date_send = timezone.now()
        q.save()

    @admin.action(description='Запустить ТЕСТ')
    def start_mailing_test(self, request, q):
        if len(q) != 1:
            return self.message_user(
                request=request,
                message='Вы можете запустить только 1 рассылку!',
                level=level.ERROR
            )
        q: MailingAllModel = q[0]
        result = mail_city_test.delay(q.id)
        print(result)


@admin.register(SegmentationModel)
class SegmentationAdmin(AbstractAdmin):
    search_fields = (
        'name',
    )


class SegmentationStepAdmin(admin.TabularInline):
    model = SegmentationStepModel
    extra = 1


@admin.register(SegmentBaseModel)
class SegmentBaseAdmin(AbstractAdmin):
    inlines = [
        SegmentationStepAdmin,
    ]
    list_display = (
        'name',
        'status',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'name',
    )
    actions = (
        'start_mailing',
        'start_mailing_test',
    )

    @admin.action(description='✔ Запустить')
    def start_mailing(
            self,
            request,
            queryset
    ):
        if len(queryset) != 1:
            return self.message_user(
                request,
                level=level.ERROR,
                message='Вы можете отправить только 1 сообщение',
            )
        result = mail_q_segment.delay(queryset[0].id, queryset[0].text)
        print(result)

    @admin.action(description='Отправить тест')
    def start_mailing_test(
            self,
            request,
            queryset
    ):
        if len(queryset) != 1:
            return self.message_user(
                request,
                level=level.ERROR,
                message='Вы можете отправить только 1 сообщение',
            )

        result = mail_q_segment_test.delay(queryset[0].id, queryset[0].text)


if DEBUG:
    @admin.register(SegmentationReadyModel)
    class SegmentationReadyAdmin(AbstractAdmin):
        pass
