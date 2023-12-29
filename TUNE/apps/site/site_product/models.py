from django.db import models

from apps.abstraction.models import AbstractModel


def path_product(
        instance,
        filename,
):
    return 'site/product/{0}/{1}/{2}'.format(
        instance.subcategory.name.replace(' ', '_'),
        instance.name.replace(' ', '_'),
        filename
    )


def path_type_product(
        instance,
        filename,
):
    return 'site/product/type/{0}'.format(
        filename
    )


class ProductColorModel(AbstractModel):
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )

    def __str__(self):
        return self.name


class ProductMemoryModel(AbstractModel):
    class Meta:
        verbose_name = 'Память'
        verbose_name_plural = 'Память'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )

    def __str__(self):
        return self.name


class ProductSizeModel(AbstractModel):
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размер'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )

    def __str__(self):
        return self.name


class ShopManufacturerModel(AbstractModel):
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )

    def __str__(self):
        return self.name


class ShopTypeModel(AbstractModel):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name='Префикс URL',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=path_type_product,
    )

    def __str__(self):
        return self.name


class ShopCategoryModel(AbstractModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )

    type = models.ForeignKey(
        verbose_name='Тип',
        to='site_product.ShopTypeModel',
        on_delete=models.CASCADE,
    )

    manufacturer = models.ForeignKey(
        verbose_name='Производитель',
        to='site_product.ShopManufacturerModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class ShopSubCategoryModel(AbstractModel):
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    category = models.ForeignKey(
        verbose_name='Производитель',
        to='site_product.ShopCategoryModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class ShopProductModel(AbstractModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    preview = models.ImageField(
        verbose_name='Превью',
        upload_to=path_product,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    amount = models.IntegerField(
        verbose_name='Цена',
    )
    subcategory = models.ForeignKey(
        verbose_name='Подкатегория',
        to='site_product.ShopSubCategoryModel',
        on_delete=models.CASCADE,
    )
    caption = models.TextField(
        verbose_name='Описание',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.save_base(self, *args, **kwargs)
        check = ShopKeyModel.objects.filter(product=self, key='slug')
        if not check:
            ShopKeyModel.objects.create(
                product=self,
                key='slug',
                value=self.subcategory.category.type.slug
            )


class ShopKeyModel(AbstractModel):
    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи'

    product = models.ForeignKey(
        verbose_name='Тип',
        to='site_product.ShopProductModel',
        on_delete=models.CASCADE,
    )

    key = models.CharField(
        verbose_name='Тип',
        max_length=255,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=255,
    )

    def __str__(self):
        return self.key


class ShopFilterParameterModel(AbstractModel):
    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    category = models.ForeignKey(
        verbose_name='Подкатегория',
        to='site_product.ShopCategoryModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.category.name
