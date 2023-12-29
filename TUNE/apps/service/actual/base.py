import re
import datetime
from pprint import pprint

from django.db.models import QuerySet

from apps.apps.configs.parameter.models import SubCategoryModel, KeyModel
from apps.apps.product.models import PriceModel
from apps.service.actual.exceptions import raise_exception
from apps.service.typing import PriceDict


class Actual:
    def __init__(
            self,
            price: PriceModel,
            request,
            admin,
    ):
        self.admin = admin
        self.request = request
        self.start_dt = datetime.datetime.utcnow()
        self.price = self.__validate_price(price)

        self.mask = self.price.category.mask.all()
        self.subcategories = self.__get_subcategories(price)
        self.keys = self.__get_keys(self.subcategories)
        self.price_list = self.__get_price_list(price)
        self.extra_mask = self.__get_extra_mask(self.subcategories)

    @staticmethod
    def __get_extra_mask(subcategories) -> list:
        out = []
        for i in subcategories:
            i: SubCategoryModel
            names = i.extra_mask.all().values('name')
            for j in names:
                out.append(j['name'])
        return out

    @staticmethod
    def __validate_price(price: PriceModel, ):
        return price

    @staticmethod
    def __get_subcategories(price: PriceModel, ) -> QuerySet[SubCategoryModel]:
        subcategories = SubCategoryModel.objects.filter(
            category=price.category,
        )
        return subcategories

    @staticmethod
    def __get_keys(subcategories: QuerySet[SubCategoryModel], ) -> dict:
        keys = KeyModel.objects.filter(subcategory__in=subcategories)
        list_keys = list(set(i.type.name for i in keys))
        out = {}
        for type_name in list_keys:
            values = []
            for key_model in keys:
                if key_model.type.name == type_name:
                    values.append(key_model)
            out[type_name] = values
        return out

    @staticmethod
    def __get_price_list(price: PriceModel, ):
        price_list = price.text.split('\r\n')
        out = []
        for i in price_list:
            if i != '':
                out.append(i)
        return out

    @staticmethod
    def __get_clear_line(line) -> str:
        return line.replace(".", "").replace(",", "").replace("-", "").lower()

    def get_amount(self, line):
        numbers = []

        line = self.__get_clear_line(line)
        matches = re.findall(r'\d+(?:\.\d+)?', line)
        for match in matches:
            numbers.append(int(match))

        if numbers:
            amount = max(numbers)
            if int(amount) < 1000:
                print("Цены нет", line.encode('utf-8'))
                return None
            return str(amount)
        else:
            print("Цены нет", line.encode('utf-8'))
            return None

    @staticmethod
    def get_value(line: str, values: list) -> str or None:
        line = line.replace(' ', '').replace('(', '').replace(')', '')
        values = [i.replace(' ', '') for i in values]
        values = sorted(values, key=len, reverse=True)
        pattern = "|".join(values)
        pattern = pattern.split('|')
        pattern = sorted(pattern, key=lambda x: len(x), reverse=True)
        pattern = '|'.join(pattern)
        pattern = pattern.replace('(', '').replace(')', '')
        keys = re.findall(pattern, line)
        if not keys:
            return None
        # return keys[0]
        return max(keys)

    def create_data(self):
        out = []
        for line in self.price_list:
            line = self.__get_clear_line(line)

            amount = self.get_amount(line)
            if not amount:
                return raise_exception(
                    self=self,
                    data=PriceDict(
                        city=self.price.region.name,
                        values={'status': False, 'type_error': 'Цена', 'line': line},
                        status=False,
                        status_code='1102'
                    )
                )
            line = line.replace(amount, '')
            values = self.get_values(line)

            if not values.status:
                return raise_exception(
                    self=self,
                    data=values
                )
            values.amount = amount
            out.append(values)

        return out

    @staticmethod
    def get_region(line) -> str:
        # regions = RegionModel.objects.all()
        # out = ''
        # for i in regions:
        #     if i.key in line:
        #         out = i.value
        # return out if out else '🇷🇺'
        return ''

    @staticmethod
    def get_markup(value):
        markup = KeyModel.objects.filter(value=value)
        return markup[0].subcategory.amount

    def get_values(self, line) -> PriceDict:
        out = {}
        for type_name, values in self.keys.items():
            values_list = [i.key.lower() for i in values]
            value = self.get_value(line=line, values=values_list)
            extra = False
            if type_name in self.extra_mask:
                for i in values:
                    if i.key.lower().replace(' ', '').replace('(', '').replace(')', '') == value:
                        value = i.value
                        out[type_name] = value
                        extra = True
            if not value and type_name in self.extra_mask:
                continue
            if not value:
                return PriceDict(
                    city=self.price.region.name,
                    values={'type_error': type_name, 'line': line},
                    status=False,
                    status_code='1101'
                )
            if not extra:
                out_value = ''
                for i in values:
                    if i.key.lower().replace(' ', '').replace('(', '').replace(')', '') == value:
                        out_value = i.value
                out[type_name] = out_value

        try:
            markup = self.get_markup(out['Серия'])
        except:
            return PriceDict(
                city=self.price.region.name,
                values={'type_error': 'Наценка', 'line': line},
                status=False,
                status_code='1101'
            )
        out['Регион'] = self.get_region(line)
        values = PriceDict(
            city=self.price.region.name,
            values=out,
            status=True,
            status_code='1000',
            markup=markup,
            price=self.price.category,
            provider=self.price.provider,
        )
        return values
