from functools import reduce
from pprint import pprint

from src.product.product_new.models import NewProductModel, ImageNewProductModel, NewProductParametersModel
import operator
from django.db.models import Q


async def get_new_product_and_image(name_or_id: str):

    if name_or_id.isnumeric():
        product = {}
        async for value_product in NewProductModel.objects.filter(
                id=name_or_id
        ).values(
            'id',
            'name',
            'amount',
            'text_post',

        ):
            product['product'] = value_product
            product['images'] = []
            async for value_image in ImageNewProductModel.objects.filter(
                    product__id=value_product['id']
            ).values():
                product['images'].append(value_image)
    else:
        product = {}
        async for value_product in NewProductModel.objects.filter(
                name=name_or_id
        ).values(
            'id',
            'name',
            'amount',
            'text_post',

        ):
            product['product'] = value_product
            product['images'] = []
            async for value_image in ImageNewProductModel.objects.filter(
                    product__id=value_product['id']
            ).values():
                product['images'].append(value_image)
    return product if product else None


async def get_new_product_names(series_name_or_id: str):
    if series_name_or_id.isnumeric():
        query = []
        async for value_product in NewProductModel.objects.filter(
                series__id=series_name_or_id,
                is_booking=False,
                is_sales=False,
                is_moderation=True
        ).values('id', 'name'):
            query.append(value_product)
        return query if query else None
    else:
        query = []
        async for value_product in NewProductModel.objects.filter(
                series__name=series_name_or_id
        ).values('id', 'name'):
            query.append(value_product)
        return query if query else None


async def get_params_new_product(name_series_or_id: str):
    query = []
    async for value_product in NewProductParametersModel.objects.filter(
            product__newproductmodel__series__name=name_series_or_id
    ).values(
        'product__newproductparametersmodel__parameter__parameter__name',
        'product__newproductparametersmodel__parameter__name'
    ).distinct():
        query.append(value_product)
    result = {}
    for data in query:
        if data['product__newproductparametersmodel__parameter__parameter__name'] in result:
            result[data['product__newproductparametersmodel__parameter__parameter__name']].append(
                data['product__newproductparametersmodel__parameter__name'])
        else:
            result[data['product__newproductparametersmodel__parameter__parameter__name']] = []
            result[data['product__newproductparametersmodel__parameter__parameter__name']].append(
                data['product__newproductparametersmodel__parameter__name'])
    return result if result else None


async def get_new_product_and_image_value(model, values):
    query = []
    q = reduce(operator.or_,
               (Q(baseproduct_ptr__name__contains=item) for item in values))

    async for value_product in NewProductModel.objects.filter(
            q
    ).values().distinct():
        check = True if (all(x in value_product['name'].split() for x in values)) else False
        if check:
            res = await get_new_product_and_image(str(value_product['id']))
            query.append(res)
    return query
