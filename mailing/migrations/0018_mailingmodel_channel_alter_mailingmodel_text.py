# Generated by Django 4.1.7 on 2023-02-19 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0008_alter_botmodel_date_last_modified_and_more'),
        ('mailing', '0017_alter_mailingmodel_date_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingmodel',
            name='channel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='channel.channelmodel', verbose_name='Канал'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailingmodel',
            name='text',
            field=models.TextField(blank=True, default='<u>Курсивный текст</u>\n<b>Жирный текст</b>\n<i>italic</i>\n<u>Подчеркнутый текст</u>\n<s>Зачеркнутый текст</s>,\n<tg-spoiler>Спрятанный текст</tg-spoiler>\n<a href="https://musthave.ru/">Ссылка на сайт</a>', help_text='Максимум 1024 симовла', max_length=1024, null=True, verbose_name='Текст'),
        ),
    ]
