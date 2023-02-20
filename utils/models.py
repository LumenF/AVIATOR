from django.core.exceptions import ObjectDoesNotExist
from django.db import models

nb = dict(null=True, blank=True)


class GetOrNoneManager(models.Manager):
    """Не возвращает ничего, если объект не существует, иначе экземпляр модели"""

    async def get_or_none(self, **kwargs):
        try:
            return await self.aget(**kwargs)
        except ObjectDoesNotExist:
            return []

    async def aget_or_none(self, **kwargs):
        try:
            return await self.aget(**kwargs)
        except ObjectDoesNotExist:
            return []

    async def afilter_or_none(self, *args, **kwargs):
        try:
            query = []
            async for value in self.filter(**kwargs).values(*args):
                query.append(value)
            return query if query else []
        except ObjectDoesNotExist:
            return []

    async def async_delete(self, **kwargs):
        #  Всегда возвращает True, выполнить проверку что пользователь есть
        try:
            return await self.filter(**kwargs).adelete()
        except ObjectDoesNotExist:
            return None
