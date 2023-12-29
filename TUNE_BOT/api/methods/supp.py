from aiogram import types

from api.methods.base import BaseAPI


class SuppProductApi(BaseAPI):
    async def get_list_type(
            self,
    ):
        """
        Получить список всех типов
        [Планшет, Телефон, ...]
        """
        response = await self.get(
            url='/Product/listType',
        )
        if response['status']:
            return response['data']
        return False

    async def get_list_manufacturer(
            self,
            type_name: str
    ):
        """
        Получить список всех производителей

        [Apple, Samsung, ...]
        """
        data = {
            'type_name': type_name,
        }
        response = await self.get(
            url='/Product/listManufacturer',
            params=data
        )
        if response['status']:
            return response['data']
        return False

    async def get_list_subcategory(
            self,
            type_name: str,
            manufacturer_name: str,
    ):
        """
        Получить список всех подкатегорий

        [iPhone 13, iPhone 14, ...]
        """
        data = {
            'type_name': type_name,
            'manufacturer_name': manufacturer_name,
        }
        response = await self.get(
            url='/Product/listSubcategory',
            params=data
        )
        if response['status']:
            return response['data']
        return False

    async def get_list_products(
            self,
            subcategory_name: str,
            tg_id: str
    ):
        """
        Получить список всех товаров

        [iPhone 13 Pro 128..., iPhone 14 Red 256..., ...]
        """
        data = {
            'subcategory_name': subcategory_name,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Product/listProducts',
            params=data
        )
        if response['status']:
            return response['data']
        elif not response['status'] and 'id' in response:
            return {'id': response['id'], 'checked': response['checked']}
        return False

    async def get_product(
            self,
            product_name: str,
            tg_id: str,
    ):
        """
        Получить товар по имени

        [iPhone 13 Pro 128..., iPhone 14 Red 256..., ...]
        """
        data = {
            'product_name': product_name,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Product/getProduct',
            params=data
        )
        if response['status']:
            return response['data']
        return False

    async def get_product_by_id(
            self,
            product_id: str,
            tg_id: str,
    ):
        """
        Получить товар по ID

        [iPhone 13 Pro 128..., iPhone 14 Red 256..., ...]
        """
        data = {
            'product_id': product_id,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Product/getProductByID',
            params=data
        )
        if response['status']:
            return response['data']
        return False

    async def get_list_sale(
            self,
    ):
        response = await self.get(
            url='/Product/listProductsSale',
        )
        if response['status']:
            return response['data']

    async def get_budget(
            self,
            min_value: str,
            max_value: str,
    ):
        data = {
            'min_value': min_value,
            'max_value': max_value,
        }
        response = await self.get(
            url='/Product/listBudgetProducts',
            params=data,
        )
        if response['status']:
            return response['data']


    async def product_like(
            self,
            name: str,
            tg_id: str,
    ):

        data = {
            'name': name,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Product/search',
            params=data,
        )
        if response['status']:
            return response['data']