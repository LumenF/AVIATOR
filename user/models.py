from typing import Union

from django.db import models, router
from django.db.models import QuerySet
from django.db.models.deletion import Collector

from service.decorators.redis import redis_delete_user
from abstractions.models import AbstractModel
from utils.models import nb


class BaseUser(AbstractModel):
    class Meta:
        abstract = True

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        **nb
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        **nb
    )

    tel = models.CharField(
        verbose_name='Телефон',
        max_length=255,
        **nb
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        **nb
    )
    is_staff = models.BooleanField(
        verbose_name='Статус админа',
        default=False,
    )
    is_ban_user = models.BooleanField(
        verbose_name='Забанен в системе',
        default=False
    )


class UserModel(BaseUser):
    class Meta:
        verbose_name = 'ТГ-Пользователь'
        verbose_name_plural = 'ТГ-Пользователи'

    telegram_id = models.CharField(
        verbose_name='ID телеграм',
        db_index=True,
        max_length=255,
        **nb
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=255,
        **nb
    )
    language_code = models.CharField(
        verbose_name='Язык',
        max_length=255,
        **nb
    )
    is_premium = models.BooleanField(
        verbose_name='Премиум',
        **nb
    )
    added_to_attachment_menu = models.BooleanField(
        verbose_name='Добавил бота в меню вложений',
        **nb
    )
    can_join_groups = models.BooleanField(
        verbose_name='Можно приглашать в группы',
        **nb
    )
    can_read_all_group_messages = models.BooleanField(
        verbose_name='Отключен режим конфиденциальности',
        **nb
    )
    supports_inline_queries = models.BooleanField(
        verbose_name='Поддерживает встроенные запросы',
        **nb
    )
    is_blocked_bot = models.BooleanField(
        verbose_name='Заблокировал бота',
        default=False,
    )
    is_bot = models.BooleanField(
        verbose_name='Это бот',
        max_length=255,
        **nb
    )
    channel = models.ForeignKey(
        verbose_name='Канал',
        to='channel.ChannelModel',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.telegram_id}'

    @classmethod
    def get_user_by_username_or_telegram_id(cls, username: Union[str, int]) -> QuerySet:
        """ Поиск пользователя в БД, возврат пользователя или None, если он не найден """
        username = str(username).replace("@", "").strip().lower()
        if username.isdigit():
            return cls.objects.filter(telegram_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @redis_delete_user
    def delete(self, using=None, keep_parents=False):
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = Collector(using=using, origin=self)
        collector.collect([self], keep_parents=keep_parents)
        return collector.delete()

    @redis_delete_user
    def save(self, *args, **kwargs):
        self.save_base(self, *args, **kwargs)
