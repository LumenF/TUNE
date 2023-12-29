import datetime

from apps.apps.configs.geography.models import CityModel
from apps.apps.logs.models import UserLogs
from apps.apps.user.models import TgUserModel
from apps.apps.user.schemas import CreateUserSchema, UpdateUserSchema


def get_user(tg_id: str) -> dict:
    user = TgUserModel.objects.filter(tg_id=tg_id).values(
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
        'city__name',
        'is_ban_user',
        'is_blocked_bot',
        'is_staff',

    ).first()
    if user:
        log = UserLogs.objects.get_or_create(
            date_created=datetime.date.today()
        )[0]

        log.update_count(user['tg_id'])
    return user

def create_user(data: CreateUserSchema):
    check = TgUserModel.objects.get_or_create(
        tg_id=data.tg_id,
        username=data.username,
        phone=data.phone,
    )
    return check[1]


def update_user(data: UpdateUserSchema):
    user_dict = dict(filter(lambda x:x[1], data.dict().items()))
    user = TgUserModel.objects.filter(tg_id=data.tg_id)
    if not user:
        return False
    user_dict['last_login'] = datetime.datetime.now()
    user.update(**user_dict)
    return True


def update_user_city(
        tg_id,
        city_name
):
    user = TgUserModel.objects.filter(tg_id=tg_id)
    if not user:
        return False
    city = CityModel.objects.filter(name=city_name)
    if not city:
        return False
    user.update(city=city[0])
    return True


def get_cities():
    cities = CityModel.objects.filter().values('name')
    if cities:
        return [i['name'] for i in cities]
    return False