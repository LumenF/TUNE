import datetime
import re

from django.db.models import Q

from apps.apps.user.models import TgUserModel
from apps.apps.logs.models import ProductLogs
from apps.apps.configs.product_conf.models import (
    ProductTypeModel,
    ProductCategoryModel,
    ProductSubCategoryModel,
)
from apps.apps.product.models import (
    ProductModel,
    FavoritesModel,
    NewProductModel,
    FavoritesSubcategoryModel,
)
from apps.apps.configs.parameter.models import (
    CategoryModel,
    SubCategoryModel,
    KeyModel,
    ProductOrderingModel,
    TypeKeyModel,
    GroupModel
)


def get_list_type() -> dict or bool:
    result = ProductTypeModel.objects.filter().values('name', 'order_id', )
    result = [i for i in result]
    if result:
        return result
    return False


def search(
        name,
        tg_id
):
    result = ProductModel.objects.filter(
        name__contains=name,
        status__in=['1', 'sale'],
    )

    if not result:
        return False
    all_out = []

    for i in result:
        out = {}
        images = [img.url for img in [i.image_1] if img]
        out['images'] = images
        out['caption'] = i.caption
        out['id'] = i.id
        out['name'] = i.name
        all_out.append(out)
    return all_out
def get_manufacturer_list(
        type_name: str,
) -> dict or bool:
    result = ProductCategoryModel.objects.filter(
        type__name=type_name
    ).values('manufacturer__name', 'manufacturer__order_id', )

    out = []
    for i in result:
        out.append(
            {
                'name': str(i['manufacturer__name']),
                'order_id': str(i['manufacturer__order_id']),
            }
        )
    if out:
        return out
    return False


def get_series_list(
        type_name: str,
        manufacturer__name: str,
) -> dict or bool:
    result = ProductSubCategoryModel.objects.filter(
        category__type__name=type_name,
        category__manufacturer__name=manufacturer__name
    ).values('name', 'order_id', )
    result = [i for i in result]
    if result:
        return result
    return False


def get_products(
        subcategory_name: str,
        user_id: str,
) -> dict or bool:
    result = ProductModel.objects.filter(
        subcategory__name=subcategory_name,
        status__in=['1', 'sale'],
    ).values('name', 'amount', )

    result = [i for i in result]
    if result:
        return result

    result = ProductSubCategoryModel.objects.filter(name=subcategory_name).values('id')
    if result:
        check = FavoritesSubcategoryModel.objects.filter(user__tg_id=user_id, subcategory__id=result[0]['id']).exists()

        out = {
            'id': result[0]['id'],
            'checked': check
        }
        return out
    return False


def get_products_sale(
) -> dict or bool:
    result = ProductModel.objects.filter(
        status__in=['sale'],
    ).values('name', 'amount', )

    result = [i for i in result]
    if result:
        return result
    return False


def get_products_budget(
        min_value: str,
        max_value: str,
) -> dict or False:
    result = ProductModel.objects.filter(
        Q(amount__range=(min_value, max_value))
        & Q(status__in=['1', 'sale'])).values_list('name', flat=True)
    result = [i for i in result]
    if result:
        return result
    return False


def get_product(
        product_name: str,
        tg_id: str,
) -> dict or bool:
    result = ProductModel.objects.filter(
        name=product_name,
        status__in=['1', 'sale'],
    ).first()

    if not result:
        return False
    view = ProductLogs.objects.get_or_create(
        date_created=datetime.date.today(),
        product=result,
    )

    if not view[1]:
        view[0].increase_count()
    user_favorite = FavoritesModel.objects.filter(
        product=result,
        user=TgUserModel.objects.get(tg_id=tg_id),
    )
    out = {
        'is_favorite': True if user_favorite else False,
    }

    images = [img.url for img in [result.image_1, result.image_2, result.image_3, ] if img]
    out['images'] = images
    out['caption'] = result.caption
    out['id'] = result.id

    return out


# def get_product_by_id(
#         product_id: str,
#         tg_id: str,
# ) -> dict or bool:
#     result = ProductModel.objects.filter(
#         id=product_id,
#         status__in=['1', 'sale'],
#     ).first()
#
#     if not result:
#         return False
#
#     user = TgUserModel.objects.filter(tg_id=tg_id)
#     out = {
#         'user': True if user else False
#     }
#
#     images = [img.url for img in [result.image_1, result.image_2, result.image_3, ] if img]
#     out['images'] = images
#     out['caption'] = result.caption
#     out['id'] = result.id
#
#     return out
#

def get_product_by_id(
        product_id: str,
        tg_id: str,
) -> dict or bool:
    result = ProductModel.objects.filter(
        id=product_id,
        status__in=['1', 'sale'],
    ).first()

    if not result:
        return False
    view = ProductLogs.objects.get_or_create(
        date_created=datetime.date.today(),
        product=result,
    )

    if not view[1]:
        view[0].increase_count()
    user_favorite = FavoritesModel.objects.filter(
        product=result,
        user=TgUserModel.objects.get(tg_id=tg_id),
    )
    out = {
        'is_favorite': True if user_favorite else False,
    }

    images = [img.url for img in [result.image_1, result.image_2, result.image_3, ] if img]
    out['images'] = images
    out['caption'] = result.caption
    out['id'] = result.id

    return out

########################################################################
# Избранное Б/У

def add_favorite(
        product_id: str,
        tg_id: str,
) -> dict or bool:
    try:
        result = FavoritesModel.objects.get_or_create(
            product=ProductModel.objects.get(id=product_id),
            user=TgUserModel.objects.get(tg_id=tg_id),
        )
        if not result[1]:
            return False
        return True
    except:
        return False


def remove_favorite(
        product_id: str,
        tg_id: str,
) -> dict or bool:
    try:
        result = FavoritesModel.objects.filter(
            product=ProductModel.objects.get(id=product_id),
            user=TgUserModel.objects.get(tg_id=tg_id),
        )
        if not result:
            return False
        result.delete()
        return True
    except:
        return False


########################################################################
# Избранное категории Б/У

def add_favorite_subcategory(
        subcategory_id: str,
        tg_id: str,
) -> dict or bool:
    try:
        result = FavoritesSubcategoryModel.objects.get_or_create(
            subcategory=ProductSubCategoryModel.objects.get(id=subcategory_id),
            user=TgUserModel.objects.get(tg_id=tg_id),
        )
        if not result[1]:
            return False
        return True
    except:
        return False


def remove_favorite_subcategory(
        subcategory_id: str,
        tg_id: str,
) -> dict or bool:
    try:
        result = FavoritesSubcategoryModel.objects.filter(
            subcategory=ProductSubCategoryModel.objects.get(id=subcategory_id),
            user=TgUserModel.objects.get(tg_id=tg_id),
        )
        if not result:
            return False
        result.delete()
        return True
    except:
        return False


########################################################################
# Новые товары


def get_list_type_new() -> dict:
    result = GroupModel.objects.filter().values('name', 'order_id', )
    result = [i for i in result]
    if result:
        return result
    return False


def get_manufacturer_list_new(
        type_name: str,
) -> dict:
    result = CategoryModel.objects.filter(
        group__name=type_name
    ).values('company__name', 'company__order_id', )

    out = []
    for i in result:
        out.append(
            {
                'name': str(i['company__name']),
                'order_id': str(i['company__order_id']),
            }
        )
    if out:
        return out
    return False


def get_series_list_new(
        type_name: str,
        manufacturer__name: str,
) -> dict:
    result = CategoryModel.objects.filter(
        group__name=type_name,
        company__name=manufacturer__name
    )
    if not result:
        return False
    check = NewProductModel.objects.filter(
        subcategory__category=result[0],
        amount__isnull=False
    )
    if not check:
        return False
    result = SubCategoryModel.objects.filter(
        category=result[0]
    ).values('name', 'order_id', )
    result = [i for i in result]
    if result:
        return result
    return False


def get_keys(
        subcategory__name: str,
):
    try:
        result = ProductOrderingModel.objects.filter(
            subcategory=SubCategoryModel.objects.get(name=subcategory__name),
            active=True,
        ).values('type__name', 'order_id')
    except:
        return False
    check = NewProductModel.objects.filter(
        subcategory=SubCategoryModel.objects.get(name=subcategory__name),
        # amount__isnull=False
    ).exclude(amount='0')
    if not check:
        return False
    out = []
    for i in result:
        out.append(
            {
                'name': i['type__name'],
                'order_id': i['order_id'],
            }
        )

    if out:
        return out
    return False


def get_key_values(
        subcategory__name: str,
        key_name: str,
):
    subcategory = SubCategoryModel.objects.get(name=subcategory__name)
    res = NewProductModel.objects.filter(
        subcategory=subcategory,
    ).exclude(amount='0').values('params', 'amount')

    out = list(set(i['params'][key_name] for i in res))
    _exit = []
    for i in out:
        result = KeyModel.objects.filter(
            subcategory=subcategory,
            value__icontains=i
        ).values('value', 'order_id').first()
        if result:
            _exit.append(
                        {
                            'name': result['value'].replace(',', ''),
                            'order_id': result['order_id'],
                        }
                    )
    if _exit:
        return _exit
    return False


def get_price(
        subcategory__name: str,
        key_dict: dict
):
    subcategory = SubCategoryModel.objects.get(name=subcategory__name)
    ordering = ProductOrderingModel.objects.filter(
        subcategory=SubCategoryModel.objects.get(name=subcategory__name)
    ).values('type__name', 'order_id')
    ordering = [i for i in ordering]
    query = Q()
    for key, value in key_dict.items():
        query &= Q(params__icontains=f'"{key}": "{value}"')

    # query = Q()
    # for key, value in key_dict.items():
    #     value = value.replace(',', '')
    #     query |= Q(params__contains={key: value})

    res = NewProductModel.objects.filter(
        query,
        subcategory=subcategory,
    ).values('params', 'amount', 'amount_sale',)
    if not res:
        return False
    products = []
    for i in res:
        if i['params'] and i['amount'] != '0':
            params = i['params']
            if int(i['amount_sale']):
                out_amount = str(int(i['amount'].replace(',', '')) - int(i['amount_sale']))
                out = '^' + i['amount'].replace(',', '') + '^ '+ out_amount + '₽'
                result = re.findall(r'\^(.*?)\^', out)[0].replace('.', '').replace(',', '').replace(' ','').replace('^', '')
                _result = ''
                for i in result:
                    _result += str('\u0336' + i + '\u0336')
                z = result.replace(result, _result).replace('^̶', '').replace('^', '')
                x = z + ' ' + out_amount + '₽'
                params['Цена'] = x
            else:
                params['Цена'] = i['amount'].replace(',', '.') + '₽'
            products.append(params)
    grouped_products = {'Цвет': []}

    for product in products:
        if 'Цвет' in product:
            color = product['Цвет']
            ordered_keys = [key_dict['type__name'] for key_dict in sorted(ordering, key=lambda x: x['order_id'])]
            values = [product.get(key, '') for key in ordered_keys]
            row = ' '.join(values)
            if color not in grouped_products:
                grouped_products[color] = []
            grouped_products[color].append(row)
        else:
            color = 'Цвет'
            ordered_keys = [key_dict['type__name'] for key_dict in sorted(ordering, key=lambda x: x['order_id'])]
            values = [product.get(key, '') for key in ordered_keys]
            row = ' '.join(values)
            grouped_products[color].append(row)

    result = ''
    for color, rows in grouped_products.items():
        result += f'\n'
        result += '\n'.join(rows) + '\n'

    text = subcategory.text.replace('%TEXT_POSITION%', result)

    return {
        'text': text,
        'image': subcategory.image.url if subcategory.image else None,
    }


def get_user_favorite(
        tg_id: str,
):
    result = FavoritesModel.objects.filter(
        user__tg_id=tg_id,
        product__status__in=['1', '2', 'sale']
    ).values('product__name')
    return [i['product__name'] for i in result]
