from django.contrib import admin
from django.core.checks import messages
from django.db import models
from django.db.models import QuerySet
from django.http import HttpRequest

from abstractions.admin import AbstractAdmin, AdminImageWidget
from mailing.models import MailingModel
from mailing.tasks import sender


@admin.register(MailingModel)
class MailingAdmin(AbstractAdmin):
    list_display = (
        'name',
        'status_send',
        'count_success',
        'count_error',
        'count_to_mailing',
        'message_id',
        'id',
    )
    exclude = (
        'count_success',
        'count_error',
        'count_to_mailing',
        'message_id',
        'id',
        'status_send'
    )
    search_fields = (
        'name',
    )

    formfield_overrides = {
        models.ImageField: {
            'widget': AdminImageWidget,
        },
    }

    autocomplete_fields = (
        'bot',
    )

    actions = (
        'start_mailing',
        'abort_mailing',
    )

    @admin.action(description='✔ Запустить')
    def start_mailing(
            self,
            request: HttpRequest,
            queryset: QuerySet
    ):
        if len(queryset) != 1:
            return self.message_user(
                request,
                level=messages.ERROR,
                message='Вы можете отправить только 1 сообщение',
            )

        result = sender.delay(queryset[0].id)
        print('result', result)

    @admin.action(description='❌ Прервать')
    def abort_mailing(
            self,
            request: HttpRequest,
            queryset: QuerySet
    ):
        queryset.update(is_moderation=True)
