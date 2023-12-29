from ninja import Schema


class GetPriceSchema(Schema):

    key_dict: dict

    subcategory__name: str
