from django.core.exceptions import ValidationError
from django.db import models

from apps.abstraction.models import AbstractModel, nb


def path_mailing(
        instance,
        filename,
):
    return 'mailing/{0}'.format(
        filename
    )


STATUS_SEND = (
    ('0', 'Не отправлено'),
    ('1', 'Процесс'),
    ('2', 'Завершено'),
    ('3', 'Прервано'),
    ('4', 'Внутренняя ошибка'),
)


class MailingAllModel(models.Model):
    class Meta:
        verbose_name = 'Рассылка всем'
        verbose_name_plural = 'Рассылка всем'

    name = models.CharField(
        verbose_name='Тема сообщения',
        max_length=255,
    )
    image_1 = models.ImageField(
        verbose_name='Изображение 1',
        upload_to=path_mailing,
        **nb
    )

    text = models.TextField(
        verbose_name='Текст',
        max_length=1024,
        help_text='Поддерживается базовая HTML разметка'
                  '<br><br>'
                  'Максимум 1024 символа',
        **nb
    )
    products = models.ManyToManyField(
        verbose_name='Товары',
        to='product.ProductModel',
        help_text='Оставьте пустым, если не требуется.',
        blank=True,
    )
    count_success = models.IntegerField(
        verbose_name='Доставлено',
        default=0,
    )
    count_fail = models.IntegerField(
        verbose_name='Ошибки',
        default=0,
    )
    count_all = models.IntegerField(
        verbose_name='Всего',
        default=0,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        default=STATUS_SEND[0][0],
        choices=STATUS_SEND,
    )
    date_send = models.DateTimeField(
        verbose_name='Дата отправки',
        null=True,
        blank=True,
    )
    redis_id = models.CharField(
        verbose_name='Идентификатор',
        max_length=255,
        **nb
    )

    def __str__(self):
        return self.name

    def get_counter(self):
        return f'{self.count_success}/{self.count_fail}/{self.count_all}'

    def clean(self):
        if (not self.image_1
                # and not self.image_2
                # and not self.image_3
                and not self.text):
            raise ValidationError(
                {
                    'image_1': 'Вы должны заполнить минимум 1 поле!',
                    # 'image_2': 'Вы должны заполнить минимум 1 поле!',
                    # 'image_3': 'Вы должны заполнить минимум 1 поле!',
                    'text': 'Вы должны заполнить минимум 1 поле!',
                },
            )


class MailingCityModel(models.Model):
    class Meta:
        verbose_name = 'Рассылка городу'
        verbose_name_plural = 'Рассылка городу'

    name = models.CharField(
        verbose_name='Тема сообщения',
        max_length=255,
    )
    image_1 = models.ImageField(
        verbose_name='Изображение 1',
        upload_to=path_mailing,
        **nb
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=1024,
        help_text='Поддерживается базовая HTML разметка'
                  '<br><br>'
                  'Максимум 1024 символа',
        **nb
    )
    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        verbose_name='Товары',
        to='product.ProductModel',
        help_text='Оставьте пустым, если не требуется.',
        blank=True,
    )
    count_success = models.IntegerField(
        verbose_name='Доставлено',
        default=0,
    )
    count_fail = models.IntegerField(
        verbose_name='Ошибки',
        default=0,
    )
    count_all = models.IntegerField(
        verbose_name='Всего',
        default=0,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        default=STATUS_SEND[0][0],
        choices=STATUS_SEND,
    )
    date_send = models.DateTimeField(
        verbose_name='Дата отправки',
        null=True,
        blank=True,
    )
    redis_id = models.CharField(
        verbose_name='Идентификатор',
        max_length=255,
        **nb
    )

    def __str__(self):
        return self.name

    def get_counter(self):
        return f'{self.count_success}/{self.count_fail}/{self.count_all}'

    def clean(self):
        if (not self.image_1
                # and not self.image_2
                # and not self.image_3
                and not self.text):
            raise ValidationError(
                {
                    'image_1': 'Вы должны заполнить минимум 1 поле!',
                    # 'image_2': 'Вы должны заполнить минимум 1 поле!',
                    # 'image_3': 'Вы должны заполнить минимум 1 поле!',
                    'text': 'Вы должны заполнить минимум 1 поле!',
                },
            )


class MailingSegmentModel(models.Model):
    class Meta:
        verbose_name = 'Рассылка сегменту'
        verbose_name_plural = 'Рассылка сегменту'

    name = models.CharField(
        verbose_name='Тема сообщения',
        max_length=255,
    )
    image_1 = models.ImageField(
        verbose_name='Изображение 1',
        upload_to=path_mailing,
        **nb
    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=1024,
        help_text='Поддерживается базовая HTML разметка'
                  '<br><br>'
                  'Максимум 1024 символа',
        **nb
    )
    segment = models.ManyToManyField(
        verbose_name='Сегменты',
        to='mailing.SegmentationModel',
        blank=False
    )
    products = models.ManyToManyField(
        verbose_name='Товары',
        to='product.ProductModel',
        help_text='Оставьте пустым, если не требуется.',
        blank=True,
    )
    count_success = models.IntegerField(
        verbose_name='Доставлено',
        default=0,
    )
    count_fail = models.IntegerField(
        verbose_name='Ошибки',
        default=0,
    )
    count_all = models.IntegerField(
        verbose_name='Всего',
        default=0,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        default=STATUS_SEND[0][0],
        choices=STATUS_SEND,
    )
    date_send = models.DateTimeField(
        verbose_name='Дата отправки',
        null=True,
        blank=True,
    )
    redis_id = models.CharField(
        verbose_name='Идентификатор',
        max_length=255,
        **nb
    )

    def __str__(self):
        return self.name

    def get_counter(self):
        return f'{self.count_success}/{self.count_fail}/{self.count_all}'

    def clean(self):
        if (not self.image_1
                and not self.text):
            raise ValidationError(
                {
                    'image_1': 'Вы должны заполнить минимум 1 поле!',
                    'text': 'Вы должны заполнить минимум 1 поле!',
                },
            )


class SegmentationModel(AbstractModel):
    class Meta:
        verbose_name = 'Сегменты аудитории'
        verbose_name_plural = 'Сегменты аудитории'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )

    def __str__(self):
        return self.name


class SegmentBaseModel(AbstractModel):
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опрос'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=STATUS_SEND,
        default=STATUS_SEND[0][0]
    )

    count_all = models.IntegerField(
        default=0,
        editable=False,
    )

    count_success = models.IntegerField(
        default=0,
        editable=False,
    )

    count_fail = models.IntegerField(
        default=0,
        editable=False,
    )

    def __str__(self):
        return self.name


class SegmentationStepModel(AbstractModel):
    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'

    base = models.ForeignKey(
        verbose_name='Определить',
        to='mailing.SegmentBaseModel',
        on_delete=models.CASCADE,
    )
    step = models.SmallIntegerField(
        verbose_name='Номер шаг',
    )
    text = models.CharField(
        verbose_name='Вопрос',
        max_length=255,
        null=True,
        blank=True,
    )

    name = models.CharField(
        verbose_name='Кнопка',
        max_length=255,

    )

    to = models.SmallIntegerField(
        verbose_name='Направить к шагу',
        null=True,
        blank=True,
    )

    finish = models.ForeignKey(
        verbose_name='Определить',
        to='mailing.SegmentationModel',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class SegmentationReadyModel(AbstractModel):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='user.TgUserModel',
        on_delete=models.CASCADE,
    )

    base = models.ForeignKey(
        verbose_name='Определить',
        to='mailing.SegmentBaseModel',
        on_delete=models.CASCADE,
    )
    segment = models.ForeignKey(
        verbose_name='Определить',
        to='mailing.SegmentationModel',
        on_delete=models.CASCADE,
    )