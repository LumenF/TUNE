from dataclasses import dataclass

from apps.apps.configs.geography.models import SuppProviderModel
from apps.apps.configs.parameter.models import CategoryModel


@dataclass
class CSVDict:
    Editions: str = None
    Parent_UID: str = None
    Price: float = None
    Tilda_UID: str = None
    Title: str = None
    row: dict = None
    headers: list = None


@dataclass
class PriceDict:
    status: bool = False
    status_code: str = '1500'

    values: dict = None
    amount: float = 0.0

    markup: int = None
    city: str = None

    price: CategoryModel = None

    provider: SuppProviderModel = None


@dataclass
class AmountDict:
    amount: str = '0.0'
    id: str = None
    values: dict = None
    title: str = None


@dataclass
class GroupDict:
    id: str = None

    amount: str = '0.0'
    values: dict = None
    title: str = None