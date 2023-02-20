from asgiref.sync import sync_to_async
from django.http import JsonResponse, HttpRequest
from ninja import Router

from user.schema import CreateUserSchema, ResponseCreateUserSchema, ResponseGetUserSchema, UpdateUserSchema

from user.service import get_user, create_user, delete_user, update_user, get_user_a_filter

router_user = Router(
    tags=['ТГ-Пользователи'],
)


@router_user.post(path="/createUser", response=ResponseCreateUserSchema)
async def create_telegram_user(
        request: HttpRequest,
        schemas: CreateUserSchema,
) -> JsonResponse:
    """Создать ТГ-Пользователя"""
    user = await create_user(schemas)
    if user:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'User created',
            },
            status=201)
    elif not user:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User already exist',
            }, status=302)


@router_user.get(path="/getUser", response=ResponseGetUserSchema)
async def get_telegram_user(
        request: HttpRequest,
        telegram_id: str,
) -> JsonResponse:
    """Получить пользователя или None, если не существует"""
    user = await get_user_a_filter(telegram_id)
    if user:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'User successfully found',
                'data': user[0],
            },
            status=200)
    elif not user:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User not found',
            },
            status=404)


@router_user.delete(path="/deleteUser")
async def delete_telegram_user(
        request: HttpRequest,
        telegram_id: str,
) -> JsonResponse:
    """Удалить пользователя"""
    user = await delete_user(telegram_id)
    if user:
        return JsonResponse(
            data={
                'status': True,
                'msg': 'User successfully delete',
            },
            status=200)
    elif not user:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User not found',
            },
            status=404)


@router_user.put(path="/updateUser")
async def update_telegram_user(
        request: HttpRequest,
        schemas: UpdateUserSchema,
) -> JsonResponse:
    """Обновить данные пользователя"""
    user = await get_user(str(schemas.telegram_id))
    if user:
        await sync_to_async(update_user, thread_sensitive=True)(user, schemas)

        return JsonResponse(
            data={
                'status': True,
                'msg': 'User successfully update',
            },
            status=200)
    elif not user:
        return JsonResponse(
            data={
                'status': False,
                'msg': 'User not found',
            },
            status=404)
