from django.http import JsonResponse
from ninja import Router
from requests import Request

from src.product.product_new.models import NewProductModel
from src.product.product_new.schema import GetNewProductByListFilterSchema
from src.product.product_new.service import get_new_product_and_image, get_params_new_product, \
    get_new_product_and_image_value

router_new_product = Router(
    tags=['Новые товары'],
)


@router_new_product.get(path='/GetNewProductBySeries', )
async def get_new_product_by_series(
        request: Request,
        series_name_or_id: str or int
) -> JsonResponse:
    """
    \nПолучить список все товары б/у по серии.

    Параметры:

    series_name_or_id = iPhone 13 Pro

    series_name_or_id = 10
    \n
    """
    if series_name_or_id.isnumeric():
        product = await NewProductModel.objects.afilter_or_none(
            series__id=series_name_or_id,
            is_active=True,
        )
    else:
        product = await NewProductModel.objects.afilter_or_none(
            series__name=series_name_or_id,
            is_active=True,
        )

    if product:
        return JsonResponse(
            data={
                'status': 'ok',
                'msg': 'New products successfully found',
                'data': {
                    'groups': product
                },
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': 'fail',
                'msg': 'New products not found',

            },
            status=404,
        )


@router_new_product.get(path='/GetNewProductByName', )
async def get_new_product_by_series(
        request: Request,
        name_or_id: str or int
) -> JsonResponse:
    """
    \nПолучить б/у товар и фото по имени.

    Параметры:

    name_or_id = iPhone 13 Pro

    name_or_id = 10
    \n
    """
    product = await get_new_product_and_image(name_or_id)
    if product:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'Support products successfully found',
                'data': product
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Support products not found',

            },
            status=404,
        )


@router_new_product.get(path='/GetListParams', )
async def get_new_product_by_series(
        request: Request,
        name_series_or_id: str or int
) -> JsonResponse:
    """
    \n Получить все парамеры серии.

    Параметры:

    name_or_id = iPhone 13 Pro

    name_or_id = 10
    \n
    """
    product = await get_params_new_product(name_series_or_id)
    if product:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'Parameters successfully found',
                'data': product
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Parameters not found',

            },
            status=404,
        )


@router_new_product.post(path='/GetNewProductByListFilter', )
async def get_new_product_by_series(
        request: Request,
        schemas: GetNewProductByListFilterSchema
) -> JsonResponse:
    """
    \nПолучить новый товар и фото по серии и списку параметров.

    Параметры:

    name_or_id = iPhone 13 Pro
    name_or_id = 10

    list_value": [
            "256",
            "Red",
            ]
    \n
    """
    model = schemas.dict_value['model']
    values = schemas.dict_value['list_value']
    product = await get_new_product_and_image_value(model, values)

    if product:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'Support products successfully found',
                'data': product
            },
            status=200,
        )
    else:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'Support products not found',

            },
            status=404,
        )
