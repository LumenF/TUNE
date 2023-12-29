import os
from pprint import pprint

import django

import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TUNE.settings")
django.setup()
from apps.apps.product.models import NewProductModel, ProductModel
from apps.apps.configs.parameter.models import KeyModel, SubCategoryModel

o = []
for i in ProductModel.objects.all().select_related():
    z = i.__dict__
    z.pop('_state')
    o.append(z)
pprint(o)