import csv
import urllib.request

from ast import literal_eval

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.abstraction.models import AbstractModel
from apps.apps.product.models import NewProductModel


def path_csv(instance,
             filename):
    return 'files/{0}/{1}'.format(
        instance.city.name,
        filename
    )


def path_subcategory(
        instance,
        filename,
):
    return 'new/subcategory/{0}/{1}'.format(
        instance.name.replace(' ', '_'),
        filename
    )


class ConfigModel(AbstractModel):
    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурация'

    TYPE_CHOICE = (
        ('bool', 'Bool'),
        ('int', 'Int'),
        ('str', 'String'),
    )

    key = models.CharField(
        verbose_name='Параметр',
        max_length=10,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=10,
    )
    type = models.CharField(
        verbose_name='Тип',
        max_length=10,
        choices=TYPE_CHOICE,
    )

    def __str__(self):
        return self.key

    def get_value(self):
        value = literal_eval(self.value)
        return value


class RegionModel(AbstractModel):
    class Meta:
        verbose_name = 'Регионы'
        verbose_name_plural = 'Регионы'

    key = models.CharField(
        verbose_name='Ключ',
        max_length=100,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=100,
    )

    def __str__(self):
        return self.key


class CSVModel(AbstractModel):
    """
    Данные CSV файла
    """

    class Meta:
        verbose_name = 'CSV'
        verbose_name_plural = 'CSV'

    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to=path_csv
    )

    def __str__(self):
        return self.city.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )
        url = self.file.url
        response = urllib.request.urlopen(url)
        lines = [i.decode('utf-8') for i in response.readlines()]

        reader = csv.DictReader(lines, delimiter=';')
        headers = []
        for key in reader:
            key: dict
            for i, value in key.items():
                headers.append(i)
            break

        # NewProductModel.objects.all().delete()
        list_id = [i['tilda_UID'] for i in NewProductModel.objects.all().values('tilda_UID')]

        to_create = []
        for row in reader:
            row: dict
            if row['Tilda UID'] not in list_id and row['Parent UID']:
                to_create.append(
                    NewProductModel(
                        tilda_UID=row['Tilda UID'],
                        title=row['Title'],
                        amount=row['Price'],
                    )
                )
        NewProductModel.objects.bulk_create(to_create)


class TypeKeyModel(AbstractModel):
    """
    Тип ключа
    Пример:
        name = Цвет
    """

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )

    def __str__(self):
        return self.name


class CompanyModel(AbstractModel):
    """
    Производители
    Пример:
        Apple
        Samsung
    """

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )
    order_id = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0
    )

    def __str__(self):
        return self.name


class GroupModel(AbstractModel):
    """
    Группы
    Пример:
        Смартфон
        Планшеты
    """

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )
    order_id = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0
    )

    def __str__(self):
        return self.name


class CategoryModel(AbstractModel):
    """
    Категории
    Пример:
        iPhone
        iPad
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )

    company = models.ForeignKey(
        verbose_name='Производитель',
        to='parameter.CompanyModel',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        verbose_name='Группа',
        to='parameter.GroupModel',
        on_delete=models.CASCADE,
    )

    mask = models.ManyToManyField(
        verbose_name='Маска',
        to='parameter.TypeKeyModel',
        help_text='Пример:<br>'
                  '-- Серия Память Цвет<br><br>'
                  'Примечание: Порядок не важен'
    )

    def __str__(self):
        return self.name


class SubCategoryModel(AbstractModel):
    """
    Подкатегории
    Пример:
        iPhone 13
        iPhone 14
        iPad Mini
    """

    class Meta:
        verbose_name = 'Подкатегории'
        verbose_name_plural = 'Подкатегории'

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=path_subcategory,
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to='parameter.CategoryModel',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Наценка',
        default=1000,
    )
    extra_mask = models.ManyToManyField(
        verbose_name='Особый атрибут',
        to='parameter.TypeKeyModel',
        blank=True,
        help_text='Пример:<br>'
                  '- Маска категории::<br>'
                  '-- Серия Память Цвет:<br><br>'
                  '- Особый атрибут:<br>'
                  '-- 2Sim:<br>',
    )
    order_id = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8),
        ]
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=300,
        default='%TEXT_POSITION%',
        help_text='Вставьте %TEXT_POSITION% в месте, где будут указаны цены.'
    )

    amount_sale = models.IntegerField(
        verbose_name='Скидка на категорию',
        default=0,
    )

    def __str__(self):
        return self.name

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )

        NewProductModel.objects.filter(
            subcategory=self
        ).update(amount_sale=self.amount_sale)


class KeyModel(AbstractModel):
    class Meta:
        verbose_name = 'Ключи поиска'
        verbose_name_plural = 'Ключи определения'

    subcategory = models.ForeignKey(
        verbose_name='Подкатегория',
        to='parameter.SubCategoryModel',
        on_delete=models.CASCADE,
    )
    key = models.CharField(
        verbose_name='Ключ',
        max_length=100,
    )

    value = models.CharField(
        verbose_name='Значение',
        max_length=100,
    )

    type = models.ForeignKey(
        verbose_name='Тип',
        to='parameter.TypeKeyModel',
        on_delete=models.CASCADE,
        related_name='types'
    )
    order_id = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8),
        ]
    )

    def __str__(self):
        return self.key


class ProductOrderingModel(models.Model):
    class Meta:
        verbose_name = 'Порядок ключей'
        verbose_name_plural = 'Порядок ключей'

    subcategory = models.ForeignKey(
        verbose_name='Подкатегория',
        to='parameter.SubCategoryModel',
        on_delete=models.CASCADE,
    )

    type = models.ForeignKey(
        verbose_name='Тип',
        to='parameter.TypeKeyModel',
        on_delete=models.CASCADE,
        related_name='types_bot'
    )

    order_id = models.IntegerField(
        verbose_name='Порядковый номер',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8),
        ]
    )
    active = models.BooleanField(
        verbose_name='Для навигации',
        default=False,

    )

    def __str__(self):
        return self.type.name
