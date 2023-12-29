from api.methods.base import BaseAPI


class LogsApi(BaseAPI):
    async def press_btn_manager(
            self,
            tg_id,
    ):
        """
        Кнопка менеджер
        """
        data = {
            'tg_id': tg_id
        }
        await self.get(
            url='/Logs/manager',
            params=data
        )

    async def press_btn_booking(
            self,
    ):
        """
        Кнопка менеджер
        """

        await self.get(
            url='/Logs/booking',
        )
