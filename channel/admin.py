from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.contrib import admin

from abstractions.admin import AbstractAdmin
from channel.models import ChannelModel, BotModel


@admin.register(ChannelModel)
class ChannelAdmin(ExtraButtonsMixin, AbstractAdmin):
    @button(
            change_form=False,
            html_attrs={
                'style':
                    'background-color: #88FF88;'
                    'color: black;'
                    'border: 2px solid black',

            },
            label='Обновить данные'
            )
    def refresh(self, request):
        self.message_user(request, 'Данные обновлены')
        return HttpResponseRedirectToReferrer(request)

    list_display = (
        'name',
        'count_members',
        'count_all_time',
        'date_last_modified',
        'date_created',
    )
    search_fields = (
        'name',
        'id_channel',
    )
    exclude = (
        'count_members',
        'count_all_time',
    )


@admin.register(BotModel)
class BotAdmin(ExtraButtonsMixin, AbstractAdmin):
    @button(
            change_form=False,
            html_attrs={
                'style':
                    'background-color: #88FF88;'
                    'color: black;'
                    'border: 2px solid black',

            },
            label='Обновить данные'
            )
    def refresh(self, request):
        self.message_user(request, 'Данные обновлены')
        return HttpResponseRedirectToReferrer(request)

    list_display = (
        'name',
        'count_members',
        'count_all_time',
        'date_last_modified',
        'date_created',
    )
    search_fields = (
        'name',
        'id_bot',
    )
    exclude = (
        'count_members',
        'count_all_time',
    )
