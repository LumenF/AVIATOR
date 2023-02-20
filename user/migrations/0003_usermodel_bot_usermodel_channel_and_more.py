# Generated by Django 4.1.7 on 2023-02-19 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0008_alter_botmodel_date_last_modified_and_more'),
        ('user', '0002_rename_tg_id_usermodel_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='bot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='channel.botmodel', verbose_name='Бот'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermodel',
            name='channel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='channel.channelmodel', verbose_name='Канал'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='date_last_modified',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Данные актуальны на'),
        ),
    ]
