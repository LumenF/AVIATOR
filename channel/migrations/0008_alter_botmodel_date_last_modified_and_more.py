# Generated by Django 4.1.7 on 2023-02-19 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0007_botmodel_count_all_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmodel',
            name='date_last_modified',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Данные актуальны на'),
        ),
        migrations.AlterField(
            model_name='channelmodel',
            name='date_last_modified',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Данные актуальны на'),
        ),
    ]