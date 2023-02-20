from datetime import datetime

from django.db import models

from abstractions.models import AbstractModel
from utils.models import nb


def path_new_image(instance,
                   filename):
    date = str(datetime.now()).replace(':', '').replace(' ', '')
    return 'mailing/{0}/{1}'.format(
        date,
        filename,
    )


default_text = '<u>Курсивный текст</u>\n' \
               '<b>Жирный текст</b>\n' \
               '<i>italic</i>\n' \
               '<u>Подчеркнутый текст</u>\n' \
               '<s>Зачеркнутый текст</s>,\n' \
               '<tg-spoiler>Спрятанный текст</tg-spoiler>\n' \
               '<a href="https://google.ru/">Ссылка</a>'


class MailingModel(AbstractModel):
    CHOICES_STATUS = [
        ('Не отправлено', 'Не отправлено'),
        ('В процессе', 'В процессе'),
        ('Завершено', 'Завершено'),
    ]

    class Meta:
        verbose_name = 'Сообщение всем'
        verbose_name_plural = 'Сообщение всем'

    name = models.CharField(
        verbose_name='Тема',
        max_length=255,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=path_new_image,
        **nb,

    )
    text = models.TextField(
        verbose_name='Текст',
        max_length=1024,
        help_text='Максимум 1024 симовла',
        default=default_text,
        **nb,
    )
    message_id = models.CharField(
        verbose_name='Идентификатор',
        max_length=255,
        **nb,
    )
    count_success = models.BigIntegerField(
        verbose_name='Доставлено',
        default=0,
    )
    count_error = models.BigIntegerField(
        verbose_name='Не дошло',
        default=0,
    )
    count_to_mailing = models.BigIntegerField(
        verbose_name='Всего',
        default=0,
    )

    status_send = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=CHOICES_STATUS,
        default='Не отправлено',
    )
    bot = models.ForeignKey(
        verbose_name='Бот для рассылки',
        to='channel.BotModel',
        on_delete=models.CASCADE,
    )

    time_start_sleep = models.TimeField(
        verbose_name='Отключить уведомления с',
        **nb
    )
    time_finish_sleep = models.TimeField(
        verbose_name='Отключить уведомления до',
        **nb
    )

    def __str__(self):
        return self.name
