# Generated by Django 4.1.7 on 2023-02-19 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0009_alter_mailing_count_error_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status_send',
            field=models.CharField(blank=True, choices=[('Не отправлено', 1), ('В процессе', 2), ('Завершено', 3)], default='Не отправлено', max_length=30, null=True, verbose_name='Статус'),
        ),
    ]
