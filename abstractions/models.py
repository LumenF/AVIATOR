from django.db import models

from utils.models import GetOrNoneManager


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        editable=True,
    )
    date_last_modified = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Данные актуальны на',
        editable=True,
    )
    objects = GetOrNoneManager()

