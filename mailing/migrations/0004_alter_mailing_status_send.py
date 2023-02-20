# Generated by Django 4.1.7 on 2023-02-19 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_alter_mailing_status_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status_send',
            field=models.CharField(choices=[(1, 'Не отправлено'), (2, 'В процессе'), (3, 'Завершено')], default=(1, 'Не отправлено'), max_length=30, verbose_name='Статус'),
        ),
    ]
