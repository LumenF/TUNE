import datetime
import json

from aiogram import types

from conf.conf_bot import api, s_storage, s_storage_user

_users = {}


def date_valid(date):
    time = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return time


class AuthService:
    def __init__(
            self,
            user: types.User,
    ):
        self.user = user

    async def get_user(self):
        """Проверить пользователя в базе"""
        # await self.check_user_redis()
        if str(self.user.id) in _users:
            last_login = _users[str(self.user.id)]['last_login']
            if last_login > datetime.datetime.utcnow():
                return _users[str(self.user.id)]
            else:
                try:
                    _users.pop(str(self.user.id))
                except:
                    pass
        await self.update_user()
        res = await api.get_user(self.user.id)
        if not res['status']:
            return False
        _users[str(self.user.id)] = {
            'data': res['data']
        }
        _users[str(self.user.id)]['last_login'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        return _users[str(self.user.id)]

    async def create_user(
            self,
            phone: str,
    ):
        """Проверить пользователя в безе"""
        res = await api.create_user(
            user=self.user,
            phone=phone
        )
        return res

    async def update_user(
            self,
    ) -> dict:
        """Проверить пользователя в безе"""
        res = await api.update_user(
            tg_id=self.user.id,
        )
        return res

    async def check_user_redis(self):
        user_id = self.user.id
        user = await s_storage_user.get(user_id)
        if user:
            user = json.loads(user)
            if 'ban' in user:
                if str(user_id) in _users:
                    _users.pop(str(user_id))
