from django.db import models

from abstractions.models import AbstractModel


class ChannelModel(AbstractModel):
    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Канал'

    name = models.CharField(
        verbose_name='Название канала',
        max_length=255,
    )
    id_channel = models.CharField(
        verbose_name='ID канала',
        max_length=255,
    )
    count_members = models.BigIntegerField(
        verbose_name='Участники',
        default=0,
    )
    count_all_time = models.BigIntegerField(
        verbose_name='За все время',
        default=0,
    )

    def __str__(self):
        return self.name


class BotModel(AbstractModel):
    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    name = models.CharField(
        verbose_name='Название бота',
        max_length=255,
    )
    id_bot = models.CharField(
        verbose_name='Токен бота',
        max_length=255,
    )
    count_members = models.BigIntegerField(
        verbose_name='Участники',
        default=0,
    )
    count_all_time = models.BigIntegerField(
        verbose_name='За все время',
        default=0,
    )

    def __str__(self):
        return self.name
