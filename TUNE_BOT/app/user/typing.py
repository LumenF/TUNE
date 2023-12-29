from dataclasses import dataclass
from pprint import pprint


@dataclass
class UserType:
    username: str

    first_name: str
    last_name: str

    email: str
    phone: str

    city: str


def get_user_type(data: dict) -> UserType:
    username = data.get('username') if data.get('username') else '<u>Не указанно</u>'
    first_name = data.get('first_name') if data.get('first_name') else '<u>Не указанно</u>'
    last_name = data.get('last_name') if data.get('last_name') else '<u>Не указанно</u>'
    phone = data.get('phone') if data.get('phone') else '<u>Не указанно</u>'
    email = data.get('email') if data.get('email') else '<u>Не указанно</u>'
    city = data.get('city__name') if data.get('city__name') else '<u>Не указанно</u>'
    user = UserType(
        username=username,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        city=city,
    )
    return user
