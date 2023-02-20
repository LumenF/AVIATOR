from django.contrib import messages
from django.http import HttpRequest

from mailing.models import MailingModel


def init_mailing(
        self,
        request: HttpRequest,
        message: MailingModel,
):
    self.message_user(
        request,
        level=messages.INFO,
        message='Рассылка запущена!',
    )
    print(message)