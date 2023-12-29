from django.db import models

from apps.abstraction.models import AbstractModel


class ProductTypeModel(AbstractModel):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        db_index=True,
    )
    order_id = models.PositiveIntegerField(
        verbose_name='Порядковый номер',
        default=0
    )

    def __str__(self):
        return self.name


class ProductManufacturerModel(AbstractModel):
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        db_index=True,
    )
    order_id = models.PositiveIntegerField(
        verbose_name='Порядковый номер',
        default=0
    )

    def __str__(self):
        return self.name


class ProductCategoryModel(AbstractModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        db_index=True,
    )
    type = models.ForeignKey(
        verbose_name='Тип',
        to='product_conf.ProductTypeModel',
        on_delete=models.CASCADE,
    )
    manufacturer = models.ForeignKey(
        verbose_name='Производитель',
        to='product_conf.ProductManufacturerModel',
        on_delete=models.CASCADE,
    )
    order_id = models.PositiveIntegerField(
        verbose_name='Порядковый номер',
        default=0
    )

    def __str__(self):
        return self.name


class ProductSubCategoryModel(models.Model):
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = (
            'name',
            'order_id'
        )

    name = models.CharField(
        verbose_name='Название',
        max_length=255,
        db_index=True,
    )
    category = models.ForeignKey(
        verbose_name='Производитель',
        to='product_conf.ProductCategoryModel',
        on_delete=models.CASCADE,
    )
    order_id = models.PositiveIntegerField(
        verbose_name='Порядковый номер',
        default=0
    )

    def __str__(self):
        return self.name


class ProductStateModel(models.Model):
    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'

    name = models.TextField(
        verbose_name='Описание',
        max_length=350,
    )

    def __str__(self):
        return self.name


class ProductGuaranteeModel(models.Model):
    class Meta:
        verbose_name = 'Гарантия'
        verbose_name_plural = 'Гарантии'

    name = models.CharField(
        verbose_name='Описание',
        max_length=255,
        db_index=True,
    )

    def __str__(self):
        return self.name


class ProductKitModel(models.Model):
    class Meta:
        verbose_name = 'Комплект'
        verbose_name_plural = 'Комплекты'
        ordering = (
            'category',
            '-name'
        )

    name = models.TextField(
        verbose_name='Описание',
        max_length=350,
    )

    category = models.ForeignKey(
        verbose_name='Категория',
        to='product_conf.ProductCategoryModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.category.name + ' | ' + self.name
