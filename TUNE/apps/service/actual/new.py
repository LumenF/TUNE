from pprint import pprint

from apps.apps.configs.parameter.models import SubCategoryModel, CategoryModel, KeyModel
from apps.apps.product.models import NewProductModel
from apps.service.typing import PriceDict


def create_data(title, tilda_UID, params, amount):
    pass


def update_data(data):
    NewProductModel.objects.filter(update=True).update(amount=0)
    products = [i['tilda_UID'] for i in NewProductModel.objects.all().values('tilda_UID')]
    updated_data = []
    for i in data:
        csv = i['csv']
        amount = csv['Price']
        price_dict: PriceDict = i['PriceDict']
        tilda_id = csv['Tilda UID']
        keys = price_dict.values
        for key, value in keys.items():
            keys[key] = value.replace(',', '')
        if tilda_id in products:
            category: CategoryModel = price_dict.price
            # sub_category = SubCategoryModel.objects.get(id=category.id)
            if 'Серия' in keys:
                series = keys['Серия']
                models_keys = KeyModel.objects.filter(
                    subcategory__category=category,
                    value=series,
                )
            else:
                models_keys = False

            if models_keys:
                model_key: KeyModel = models_keys[0]
                updated_data.append(
                    NewProductModel(
                        tilda_UID=tilda_id,
                        amount=amount,
                        params=keys,
                        subcategory=model_key.subcategory
                    )
                )
            else:
                updated_data.append(
                    NewProductModel(
                        tilda_UID=tilda_id,
                        amount=amount,
                        params=keys,
                    )
                )
    NewProductModel.objects.bulk_update(updated_data, ['amount', ])
