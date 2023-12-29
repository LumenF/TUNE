import datetime
from typing import Optional

from ninja import Schema


class CreateUserSchema(Schema):

    tg_id: int

    username: Optional[str] = None

    phone: Optional[str] = None


class UpdateUserSchema(Schema):
    tg_id: str

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    phone: Optional[str] = None
    email: Optional[str] = None
