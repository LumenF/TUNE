from pprint import pprint
from typing import List

import requests

from TUNE.settings import TUNE_BASE_URL
from apps.apps.product.models import NewProductModel
from apps.apps.product.types import CatalogItem


def get_catalog() -> List[CatalogItem]:
    try:
        url = f'{TUNE_BASE_URL}index.php?route=api/all/get_catalog&token=A0kwh2L8KRzha3zicpT6VJYEMq47RTU7&limit=10000'
        result = requests.get(
            url=url
        )
        out = []
        for i in result.json()['products']:
            out.append(
                CatalogItem(
                    name=i['name'],
                    product_id=int(i['product_id']),
                    provider_id=int(i['supplier_id']),
                )
            )

        return out
    except:
        return None


def create_new_catalog_item(catalog: List[CatalogItem]):
    """
    Создать товары в NewProductModel если их нет
    """

    list_ids = [int(i['tilda_UID']) for i in NewProductModel.objects.all().values('tilda_UID')]
    to_create: List[NewProductModel] = []
    for i in catalog:
        if i.product_id not in list_ids:
            to_create.append(
                NewProductModel(
                    title=i.name,
                    tilda_UID=i.product_id,
                    amount=0,
                    amount_sale=0
                )
            )
    NewProductModel.objects.bulk_create(to_create)

    to_update: List[NewProductModel] = []
    for i in catalog:
        if i.product_id in list_ids:
            to_update.append(
                NewProductModel(
                    title=i.name,
                    tilda_UID=i.product_id,
                    amount=0,
                    amount_sale=0
                )
            )
    update_fields = ['title', ]

    NewProductModel.objects.bulk_update(to_update, fields=update_fields)


    return len(to_create)


