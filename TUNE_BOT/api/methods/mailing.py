from api.methods.base import BaseAPI


class MailingApi(BaseAPI):
    async def mail_all(
            self,
            mail_id: str,
    ) -> list or False:
        """
        Получить список всех товаров в рассылке всем
        """
        data = {
            'mail_id': mail_id,
        }
        response = await self.get(
            url='/Mail/all',
            params=data,
        )
        if response['status']:
            return response['data']
        return False

    async def mail_city(
            self,
            mail_id: str,
    ) -> list or False:
        """
        Получить список всех товаров в рассылке по городу
        """
        data = {
            'mail_id': mail_id,
        }
        response = await self.get(
            url='/Mail/city',
            params=data,
        )
        if response['status']:
            return response['data']
        return False

    async def get_quiz(
            self,
            segmentation_id: str
    ) -> dict or bool:
        """
        Получить все шаги
        :return:
        """
        data = {
            'segmentation_id': segmentation_id
        }
        response = await self.get(
            url='/Quiz/getQuiz',
            params=data
        )

        if response['status']:
            return response

    async def set_quiz_result(
            self,
            segmentation_name: str,
            tg_id: str,
            quiz_id: str,

    ) -> dict or bool:
        """
        Записать результат опроса
        :return:
        """
        data = {
            'segmentation_name': segmentation_name,
            'tg_id': tg_id,
            'quiz_id': quiz_id,
        }
        response = await self.get(
            url='/Quiz/setQuizResult',
            params=data
        )

        if response['status']:
            return response