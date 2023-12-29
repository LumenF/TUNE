from api.methods.base import BaseAPI


class FavoriteApi(BaseAPI):
    async def add_favorite(
            self,
            product_id: str,
            tg_id: str,
    ):
        """
        Добавить в избранное Б/У
        """
        data = {
            'product_id': product_id,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Favorite/addFavorite',
            params=data,
        )
        if response['status']:
            return True
        return False

    async def remove_favorite(
            self,
            product_id: str,
            tg_id: str,
    ):
        """
        Удалить из избранного Б/У
        """
        data = {
            'product_id': product_id,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Favorite/removeFavorite',
            params=data
        )

        if response['status']:
            return True
        return False

    async def add_favorite_category(
            self,
            subcategory_id: str,
            tg_id: str,
    ):
        """
        Добавить в избранное категорию Б/У
        """
        data = {
            'subcategory_id': subcategory_id,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Favorite/addFavoriteSubcategory',
            params=data,
        )
        if response['status']:
            return True
        return False

    async def remove_favorite_category(
            self,
            subcategory_id: str,
            tg_id: str,
    ):
        """
        Удалить из избранного категорию Б/У
        """
        data = {
            'subcategory_id': subcategory_id,
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Favorite/removeFavoriteSubcategory',
            params=data
        )

        if response['status']:
            return True
        return False

    async def get_user_favorite(
            self,
            tg_id: str,
    ):
        data = {
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Favorite/getUserFavorite',
            params=data
        )
        return response

    async def get_bonus(
            self,
            tg_id: str,
    ):
        data = {
            'tg_id': tg_id,
        }
        response = await self.get(
            url='/Invited/bonus',
            params=data
        )
        return response

