from aiogram import types

from api.methods.base import BaseAPI


class NewProductApi(BaseAPI):
    async def get_new_list_type(
            self,
    ):
        response = await self.get(
            url='/NewProduct/listType',
        )
        if response['status']:
            return response['data']

    async def get_new_list_manufacturer(
            self,
            type_name: str,
    ):
        params = {
            'type_name': type_name,
        }
        response = await self.get(
            url='/NewProduct/listManufacturer',
            params=params
        )
        if response['status']:
            return response['data']

    async def get_new_list_subcategory(
            self,
            type_name: str,
            manufacturer_name: str
    ):
        params = {
            'type_name': type_name,
            'manufacturer_name': manufacturer_name,
        }
        response = await self.get(
            url='/NewProduct/listSubcategory',
            params=params
        )
        if response['status']:
            return response['data']

    async def get_new_keys(
            self,
            subcategory__name: str,
    ):
        params = {
            'subcategory__name': subcategory__name,
        }
        response = await self.get(
            url='/NewProduct/getKeys',
            params=params
        )
        if response['status']:
            return response['data']

    async def get_new_list_keys_values(
            self,
            subcategory__name: str,
            key_name: str,
    ):
        params = {
            'subcategory__name': subcategory__name,
            'key_name': key_name,
        }
        response = await self.get(
            url='/NewProduct/listKeyValues',
            params=params
        )
        if response['status']:
            return response['data']

    async def post_values_keys(
            self,
            subcategory__name: str,
            key_dict: dict,
    ):
        data = {
            'subcategory__name': subcategory__name,
            'key_dict': key_dict,
        }

        response = await self.post(
            url='/NewProduct/getPrice',
            data=data
        )
        if response['status']:
            return response['data']

