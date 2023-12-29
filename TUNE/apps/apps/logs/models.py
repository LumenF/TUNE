from django.db import models

from apps.abstraction.models import AbstractModel


class CSVLogs(AbstractModel):
    class Meta:
        verbose_name = 'Актуализация'
        verbose_name_plural = 'Актуализация'

    file = models.FileField(
        verbose_name='Файл',
    )

    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.date_created)


class UserLogs(models.Model):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    date_created = models.DateField(
        verbose_name='Дата',
        auto_now=True
    )

    count = models.IntegerField(
        verbose_name='Кол-во',
        default=0,
    )

    users = models.JSONField(
        verbose_name='Пользователи',
        null=True
    )

    def __str__(self):
        return str(self.date_created)

    def update_count(self, tg_id):
        if self.users is None:
            self.users = []
        if tg_id in self.users:
            pass
        else:
            users: list = self.users
            users.append(tg_id)
            self.users = users
            self.count += 1
            self.save()


class ProductLogs(models.Model):
    class Meta:
        verbose_name = 'Б/У Товары'
        verbose_name_plural = 'Б/У Товары'

    date_created = models.DateField(
        verbose_name='Дата',
        editable=True
    )

    count = models.IntegerField(
        verbose_name='Кол-во',
        default=1,
    )

    product = models.ForeignKey(
        verbose_name='Товар',
        to='product.ProductModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.date_created)

    def increase_count(self):
        self.count += 1
        self.save_base()


class AmountProductLogs(models.Model):
    class Meta:
        verbose_name = 'Продажи Б/У Товары'
        verbose_name_plural = 'Продажи Б/У Товары'

    date_created = models.DateField(
        verbose_name='Дата',
        editable=True
    )

    amount = models.IntegerField(
        verbose_name='Сумма дня',
        default=0,
    )

    product = models.ManyToManyField(
        verbose_name='Товар',
        to='product.ProductModel',
    )

    def __str__(self):
        return str(self.date_created)


class ChapterLogs(models.Model):
    class Meta:
        verbose_name = 'Разделы'
        verbose_name_plural = 'Разделы'

    date_created = models.DateField(
        verbose_name='Дата',
        editable=True,
        db_index=True,
    )

    chapter = models.CharField(
        verbose_name='Раздел',
        max_length=255,
    )
    button = models.CharField(
        verbose_name='Раздел',
        max_length=255,
    )

    count = models.IntegerField(
        verbose_name='Кол-во',
        default=1
    )

    def __str__(self):
        return str(self.date_created)

    def increase_count(self):
        self.count += 1
        self.save_base()


class ManagerLogs(models.Model):
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджер'

    date_created = models.DateField(
        verbose_name='Дата',
        editable=True,
        db_index=True,
    )

    count = models.IntegerField(
        verbose_name='Кол-во',
        default=1
    )

    users = models.JSONField(
        verbose_name='Пользователи',
        null=True,
    )

    def __str__(self):
        return str(self.date_created)

    def increase_count(self):
        self.count += 1
        self.save_base()

    def update_count(self, tg_id):
        if self.users is None:
            self.users = []
        if tg_id in self.users:
            pass
        else:
            users: list = self.users
            users.append(tg_id)
            self.users = users
            self.count += 1
            self.save()


class BookingProductLogs(models.Model):
    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Бронь'

    date_created = models.DateField(
        verbose_name='Дата',
        editable=True,
        db_index=True,
    )

    count = models.IntegerField(
        verbose_name='Кол-во',
        default=1
    )

    def __str__(self):
        return str(self.date_created)

    def increase_count(self):
        self.count += 1
        self.save_base()
