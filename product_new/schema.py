from typing import Optional

from ninja import Schema


class GetNewProductByListFilterSchema(Schema):
    dict_value: dict
