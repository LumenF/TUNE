from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

nb = dict(null=True, blank=True)


class GetOrNoneManager(models.Manager):
    """Не возвращает ничего, если объект не существует, иначе экземпляр модели"""

    async def aget_or_none(self, **kwargs):
        try:
            return await self.aget(**kwargs)
        except ObjectDoesNotExist:
            return []

    async def afilter(self, queryset):
        return await sync_to_async(list)(queryset)
    # async def afilter_or_none(self, *args, **kwargs):
    #     try:
    #         query = []
    #         async for value in self.filter(**kwargs).values(*args):
    #             query.append(value)
    #         return query if query else []
    #     except ObjectDoesNotExist:
    #         return []


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    date_created = models.DateField(
        auto_now=True,
        verbose_name='Дата создания',
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
    # objects = GetOrNoneManager()
