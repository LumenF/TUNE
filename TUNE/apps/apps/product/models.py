import datetime
import re
from email.policy import default

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from apps.abstraction.models import AbstractModel, nb
from apps.apps.logs.models import AmountProductLogs

BASE_TEXT = '\nДоступен trade-in ♻️' \
            '\n(Сдаете старое устройство - получаете скидку на новое)' \
            '\n\nСамовывоз:' \
            '\n- г. СПБ, ул. Восстания 7, БЦ «Андреевский», офис 208' \
            '\n- г. Москва, Барклая, 6, стр. 3, офис 104' \
            '\n\nБыстрая и безопасная доставка по России и странам СНГ🚀'


class PriceModel(AbstractModel):
    class Meta:
        verbose_name = 'Прайс'
        verbose_name_plural = 'Прайсы'

    category = models.ForeignKey(
        verbose_name='Категории товаров',
        to='parameter.CategoryModel',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Прайс',
    )

    region = models.ForeignKey(
        verbose_name='Регион прайса',
        to='geography.CityModel',
        on_delete=models.CASCADE,
        default=1,
    )

    provider = models.ForeignKey(
        verbose_name='Поставщик',
        to='geography.SuppProviderModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.category.name


def save_path(instance, filename):
    return 'device/{0}/{1}/{2}'.format(
        instance.subcategory.category.name.replace(' ', '_'),
        instance.subcategory.name.replace(' ', '_'),
        filename,
    )


def get_date(line):
    line = str(line)
    date_list = line.split('-')
    return '-'.join(date_list[::-1])


class ProductModel(AbstractModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    STATUS_CHOICES = (
        ('0', 'Модерация'),
        ('1', 'Опубликовано'),
        ('sale', 'Скидка'),
        ('2', 'Забронировано'),
        ('3', 'Продано в телеграм'),
        ('4', 'Продано в инстаграм'),
        ('5', 'Продано в магазине'),
    )
    image_1 = models.ImageField(
        verbose_name='Картинка',
        upload_to=save_path,
    )
    image_2 = models.ImageField(
        verbose_name='Картинка',
        upload_to=save_path,
        **nb,
    )
    image_3 = models.ImageField(
        verbose_name='Картинка',
        upload_to=save_path,
        **nb,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=90,
        db_index=True,
        help_text='Название должно содержать конечную цену'
                  '<br><br>Цена не должна содержать пробелы'
                  '<br><br>Для перечеркивания цены, оберните её в ^1000^'
                  '<br><br>🔥 ⚡️ 💥 ₽ 🔻 ✅ 🔝'
    )
    amount_buy = models.BigIntegerField(
        verbose_name='Цена закупки',
        help_text='Цена закупки без наценки.',
    )
    amount = models.BigIntegerField(
        verbose_name='Цена',
        **nb,
    )
    code = models.CharField(
        verbose_name='Код товара',
        max_length=30,
    )
    amount_sale = models.IntegerField(
        verbose_name='Скидка',
        default=0,
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )
    state = models.ForeignKey(
        verbose_name='Состояние',
        to='product_conf.ProductStateModel',
        on_delete=models.CASCADE,
    )
    kit = models.ForeignKey(
        verbose_name='Комплект',
        to='product_conf.ProductKitModel',
        on_delete=models.CASCADE,
    )
    guarantee = models.ForeignKey(
        verbose_name='Гарантия',
        to='product_conf.ProductGuaranteeModel',
        on_delete=models.CASCADE,
        **nb,
    )
    custom_guarantee = models.DateField(
        verbose_name='Своя гарантия',
        **nb,
    )
    subcategory = models.ForeignKey(
        verbose_name='Категория',
        to='product_conf.ProductSubCategoryModel',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Комментарий',
        max_length=700,
        help_text='Оставить поле пустым, если не требуется.',
        **nb,
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to='user.UserModel',
        on_delete=models.CASCADE,
        blank=True,
    )
    caption = models.TextField(
        verbose_name='Итоговый текст',
        max_length=1024,
        **nb,
    )

    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE,
        default=1
    )

    date_sale = models.DateField(
        verbose_name='Дата продажи',
        **nb,
    )
    create = models.BooleanField(
        verbose_name='Создано',
        default=False,
    )

    def __str__(self):
        return self.name

    def clean(self):
        # try:
        name = self.name.replace('.', '').replace(',', '')
        numbers = re.findall(r'\d+(?:[.,]\d+)?', name)
        prices = [int(num) for num in numbers]
        prices = prices[-1]

        if int(prices) < 1000:
            raise ValidationError({'name': 'Не найдена цена'})

        if str(self.amount) != str(prices):
            if self.create:
                from apps.apps.product.tasks import send_message_amount_change
                send_message_amount_change.delay(_id=self.id)
        self.amount = str(prices)
        #
        # except:
        #     raise ValidationError({'name': 'Не найдена цена'})

        if self.guarantee and self.custom_guarantee:
            raise ValidationError(
                {
                    'guarantee': 'Выберите только 1 значение',
                    'custom_guarantee': 'Выберите только 1 значение'
                },
            )
        if not self.guarantee and not self.custom_guarantee:
            raise ValidationError(
                {
                    'guarantee': 'Выберите 1 из полей',
                    'custom_guarantee': 'Выберите 1 из полей'
                },
            )

    def save(self, *args, **kwargs):

        text = ''

        if self.name.count('^') == 2:
            result = re.findall(r'\^(.*?)\^', self.name)[0].replace('.', '').replace(',', '').replace(' ', '').replace(
                '^', '')
            _result = ''
            for i in result:
                _result += str('\u0336' + i + '\u0336')
            self.name = self.name.replace(result, _result).replace('^̶', '').replace('^', '')

        text += '<b>' + self.name + '</b>'
        text += '\n\nКомплект: ' + self.kit.name
        text += '\n\nСостояние: \n' + self.state.name
        text += '\n\nКод товара: ' + self.code

        if self.text:
            text += '\n\n' + self.text

        if self.custom_guarantee:
            text += '\n\nГарантия до: ' + get_date(self.custom_guarantee)
        if self.guarantee:
            text += '\n\n' + str(self.guarantee)

        text += '\n' + BASE_TEXT
        self.caption = text
        if self.status in ['3', '4', '5']:
            if not self.date_sale:
                self.date_sale = datetime.date.today()
        else:
            self.date_sale = None

        self.save_base(*args, **kwargs)
        if not self.create and self.status in ['1', 'sale'] and self.author.groups.all() not in ['Поставщик']:
            self.create = True
            self.save_base(*args, **kwargs)
            from apps.apps.product.tasks import send_message_add_category
            send_message_add_category.delay(_id=self.id)


class FavoritesModel(AbstractModel):
    class Meta:
        verbose_name = 'Избранное Б/У'
        verbose_name_plural = 'Избранные Б/У'

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='user.TgUserModel',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        verbose_name='Товар',
        to='product.ProductModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.product.name


class FavoritesSubcategoryModel(AbstractModel):
    class Meta:
        verbose_name = 'Избранное категории Б/У'
        verbose_name_plural = 'Избранные категории Б/У'

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to='user.TgUserModel',
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(
        verbose_name='Товар',
        to='product_conf.ProductSubCategoryModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.subcategory.name


class NewProductModel(AbstractModel):
    class Meta:
        verbose_name = 'Новые товары'
        verbose_name_plural = 'Новые товары'

    subcategory = models.ForeignKey(
        verbose_name='Категория',
        to='parameter.SubCategoryModel',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    tilda_UID = models.BigIntegerField(
        verbose_name='Новый сайт ID',
        primary_key=True,
        unique=True
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=500,
    )
    amount = models.CharField(
        verbose_name='Цена',
        max_length=255,
    )
    amount_sale = models.CharField(
        verbose_name='Скидка',
        max_length=255,
        default=0
    )
    params = models.JSONField(
        verbose_name='Ключи',
        null=True,
        blank=True,
    )
    update = models.BooleanField(
        verbose_name='Обновлять?',
        default=True,
    )

    provider = models.ForeignKey(
        verbose_name='Поставщик',
        to='geography.SuppProviderModel',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    tilda_id = models.CharField(
        max_length=255,
        verbose_name='ID Тильды',
        null=True,
        blank=True,
    )
    def __str__(self):
        return self.title


class NewPriceSearchModel(AbstractModel):
    class Meta:
        verbose_name = 'Цены поставщиков'
        verbose_name_plural = 'Цены поставщиков'

    amount = models.CharField(
        verbose_name='Цена',
        max_length=255,
    )
    markup = models.CharField(
        verbose_name='Наценка устройства',
        max_length=255,
    )
    params = models.JSONField(
        verbose_name='Ключи',
        null=True,
        blank=True,
    )

    provider = models.ForeignKey(
        verbose_name='Поставщик',
        to='geography.SuppProviderModel',
        on_delete=models.CASCADE,
    )

    city = models.ForeignKey(
        verbose_name='Город',
        to='geography.CityModel',
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        return self.provider.name
