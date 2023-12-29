from aiogram import types

from api.methods.base import BaseAPI


class UserApi(BaseAPI):

    async def set_invited(
            self,
            url: str,
    ):
        params = {
            'url': url,
        }

        response = await self.get(
            url='/Invited/set',
            params=params
        )
        return response

    async def get_user(
            self,
            tg_id: str,
    ):
        params = {
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/User/getUser',
            params=params
        )
        return response

    async def create_user(
            self,
            user: types.User,
            phone: str,
    ):
        data = {
            'tg_id': user.id,
            'username': user.username,
            'phone': phone,
        }

        response = await self.post(
            url='/User/createUser',
            data=data
        )
        return response

    async def update_user(
            self,
            tg_id: str,
            username: str = '',
            first_name: str = '',
            last_name: str = '',
            phone: str = '',
            email: str = '',
    ):
        data = {
            'tg_id': str(tg_id),
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        response = await self.put(
            url='/User/updateUser',
            data=data
        )
        return response

    async def get_cities(
            self,
    ):
        response = await self.get(
            url='/User/getCities',
        )
        return response

    async def update_user_city(
            self,
            tg_id: str,
            city_name: str,
    ):
        data = {
            'tg_id': tg_id,
            'city_name': city_name,
        }
        response = await self.get(
            url='/User/updateUserCity',
            params=data
        )
        return response

