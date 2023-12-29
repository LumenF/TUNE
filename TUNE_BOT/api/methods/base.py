import os

import aiohttp


class BaseAPI:
    BASE_URL = f'http://{os.getenv("BACKEND_URL")}:8000/api'
    HEADERS = {
        'Authorization': f'Bearer {os.getenv("BACKEND_ACCESS_TOKEN")}',
        'content_type': 'application/json',
    }

    async def post(
            self,
            url: str,
            data: dict = None,
    ):
        """
        :param url: URL метода, начинается с /
        :param data: Список данных
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.BASE_URL}' + url,
                                    headers=self.HEADERS,
                                    json=data
                                    ) as resp:
                print(await resp.text())
                return await resp.json()

    async def put(
            self,
            url: str,
            data: dict = None,
    ):
        """
        :param url: URL метода, начинается с /
        :param data: Список данных
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.put(f'{self.BASE_URL}' + url,
                                   headers=self.HEADERS,
                                   json=data
                                   ) as resp:
                return await resp.json()

    async def get(
            self,
            url: str,
            params: dict = None,
    ):
        """
        :param url: URL метода, начинается с /
        :param params:
        :return: Словарь параметров
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.BASE_URL}' + url,
                                   headers=self.HEADERS,
                                   params=params,
                                   ) as resp:

                return await resp.json()
