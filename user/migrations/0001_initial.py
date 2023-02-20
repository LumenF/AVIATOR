# Generated by Django 4.1.5 on 2023-01-27 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_last_modified', models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего действия')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия')),
                ('tel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Статус админа')),
                ('is_ban_user', models.BooleanField(default=False, verbose_name='Забанен в системе')),
                ('tg_id', models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True, verbose_name='ID телеграм')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ник')),
                ('language_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Язык')),
                ('is_premium', models.BooleanField(blank=True, null=True, verbose_name='Премиум')),
                ('added_to_attachment_menu', models.BooleanField(blank=True, null=True, verbose_name='Добавил бота в меню вложений')),
                ('can_join_groups', models.BooleanField(blank=True, null=True, verbose_name='Можно приглашать в группы')),
                ('can_read_all_group_messages', models.BooleanField(blank=True, null=True, verbose_name='Отключен режим конфиденциальности')),
                ('supports_inline_queries', models.BooleanField(blank=True, null=True, verbose_name='Поддерживает встроенные запросы')),
                ('is_blocked_bot', models.BooleanField(default=False, verbose_name='Заблокировал бота')),
                ('is_bot', models.BooleanField(blank=True, max_length=255, null=True, verbose_name='Это бот')),
            ],
            options={
                'verbose_name': 'ТГ-Пользователь',
                'verbose_name_plural': 'ТГ-Пользователи',
            },
        ),
    ]