# Generated by Django 4.1.7 on 2023-02-19 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_last_modified', models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего действия')),
            ],
            options={
                'verbose_name': 'Канал',
                'verbose_name_plural': 'Канал',
            },
        ),
    ]
