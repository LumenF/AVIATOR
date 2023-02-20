import datetime
import json
from typing import Any

from asgiref.sync import sync_to_async

from AVIATOR.settings import s_redis_user
from channel.models import ChannelModel
from user.models import UserModel


def get_telegram_user(schemas) -> [UserModel]:
    """Получить пользователя или None, если не существует"""
    try:
        user = UserModel.objects.get(
            telegram_id=schemas.telegram_id,
            channel=ChannelModel.objects.get(id=schemas.channel),
        )
        return True
    except:
        return False


def create_telegram_user(data) -> [UserModel]:
    """Создать пользователя"""
    try:
        user = UserModel.objects.create(
            telegram_id=data.telegram_id,
            first_name=data.first_name,
            last_name=data.last_name,
            tel=data.tel,
            email=data.email,
            username=data.username,
            language_code=data.language_code,
            is_premium=data.is_premium,
            added_to_attachment_menu=data.added_to_attachment_menu,
            can_join_groups=data.can_join_groups,
            can_read_all_group_messages=data.can_read_all_group_messages,
            supports_inline_queries=data.supports_inline_queries,
            is_bot=data.is_bot,
            date_created=datetime.datetime.utcnow(),
            date_last_modified=datetime.datetime.utcnow(),
            channel=ChannelModel.objects.get(id=data.channel),
        )
        return True
    except:
        return False


async def get_user(telegram_id: str) -> [UserModel]:
    """Получить пользователя или None, если не существует"""
    user = await UserModel.objects.aget_or_none(
        telegram_id=telegram_id
    )
    return user


async def get_user_a_filter(telegram_id: str) -> [UserModel]:
    """Получить пользователя или None, если не существует"""
    user = await UserModel.objects.afilter_or_none(
        telegram_id=telegram_id
    )
    return user


def update_user(user: UserModel, schemas):
    """Обновить пользователя"""
    for attr, value in schemas.dict().items():
        update_user_redis(telegram_id=schemas.telegram_id,
                          field_name=attr,
                          field_value=value,
                          )

        if value:
            update_user_redis(telegram_id=schemas.telegram_id,
                              field_name=attr,
                              field_value=value,
                              )
            setattr(user, attr, value)
    user.save()
    s_redis_user.delete(user.telegram_id)


async def delete_user(telegram_id: str) -> [UserModel]:
    """Удалить пользователя или None, если не существует"""
    user = await UserModel.objects.async_delete(
        telegram_id=telegram_id
    )
    s_redis_user.delete(telegram_id)
    return user


async def create_user(data):
    """Создать пользователя"""

    user = await sync_to_async(get_telegram_user, thread_sensitive=True)(data)
    if not user:
        user = await sync_to_async(create_telegram_user, thread_sensitive=True)(data)
        return True

    return False


def update_user_redis(telegram_id: int,
                      field_name: str,
                      field_value: Any,
                      ):
    """Получить данные пользователя из REDIS"""
    user = s_redis_user.get(telegram_id)
    if not user:
        return False
    user = json.loads(user)
    user[field_name] = field_value
    s_redis_user.set(
        telegram_id,
        json.dumps(user, indent=4, sort_keys=True, default=str),
    )


def delete_user_redis(telegram_id: int):
    """Удалить данные пользователя из REDIS"""
    user = s_redis_user.get(telegram_id)
    if not user:
        return False
    user = s_redis_user.delete(telegram_id)
