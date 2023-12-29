from collections import OrderedDict

import django_filters
from django import forms
from django_filters.utils import get_model_field

from django_filters.widgets import RangeWidget

from apps.site.site_product.models import ShopProductModel, ShopSubCategoryModel


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = ShopProductModel
        fields = [
            'subcategory',
        ]

    subcategory = django_filters.ModelMultipleChoiceFilter(
        queryset=ShopSubCategoryModel.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    def qs(self):
        if not hasattr(self, "_qs"):
            self._qs = self.queryset.all()
            self.amount = django_filters.RangeFilter(field_name='amount',
                                                     widget=RangeWidget(
                                                         attrs={'class': 'form-control', 'id': 'amount'}))
        return self._qs
