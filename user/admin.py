from django.contrib import admin
from django.contrib import messages

from service.decorators.redis import redis_delete_user
from abstractions.admin import AbstractAdmin
from user.models import UserModel
from user.service import update_user_redis


@admin.register(UserModel)
class UserAdmin(AbstractAdmin):
    fields = (
        'telegram_id',
        'username',
        'first_name',
        'last_name',
        'bot',
        'is_staff',
        'is_blocked_bot',
        'is_ban_user',
    )
    readonly_fields = (
        'is_staff',
        'is_blocked_bot',
        'is_ban_user',
    )
    actions = (
        'ban_user',
        'unban_user',
        'add_admin',
        'remove_admin',
    )
    list_display = (
        '__str__',
        'bot',
        'tel',
        'is_blocked_bot',
        'is_ban_user',
        'is_staff',
        'date_created',
        'date_last_modified',)
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'tel',
        'telegram_id',
        'email',
    )
    list_filter = (
        'is_staff',
        'is_blocked_bot',
        'is_ban_user',
    )
    autocomplete_fields = (
        'bot',
    )

    @admin.action(description='Забанить пользователя')
    def ban_user(self, request, queryset):
        queryset.update(is_ban_user=True)
        for user in queryset:
            update_user_redis(
                telegram_id=user.telegram_id,
                field_name='is_ban_user',
                field_value=True
            )
        self.message_user(
            request=request,
            message='Успешно забанен',
            level=messages.INFO
        )

    @admin.action(description='Разбанить пользователя')
    def unban_user(self, request, queryset):
        queryset.update(is_ban_user=False)
        for user in queryset:
            update_user_redis(
                telegram_id=user.telegram_id,
                field_name='is_ban_user',
                field_value=False
            )
        self.message_user(
            request=request,
            message='Успешно снят бан',
            level=messages.INFO
        )

    @admin.action(description='Дать админ-права')
    def add_admin(self, request, queryset):
        queryset.update(is_staff=True)
        for user in queryset:
            update_user_redis(
                telegram_id=user.telegram_id,
                field_name='is_staff',
                field_value=True
            )
        self.message_user(
            request=request,
            message='Права успешно выданы',
            level=messages.WARNING
        )

    @admin.action(description='Забрать админ-права')
    def remove_admin(self, request, queryset):
        queryset.update(is_staff=False)
        for user in queryset:
            update_user_redis(
                user_id=user.telegram_id,
                field_name='is_staff',
                field_value=False
            )
        self.message_user(
            request=request,
            message='Права успешно отозваны',
            level=messages.INFO
        )

    @redis_delete_user
    def delete_model(self, request, obj):
        obj.delete()
