
import telebot

from AVIATOR.celery import app
from channel.models import BotModel
from mailing.models import MailingModel
from service.bot.sender import sender_master
from user.models import UserModel


class BotClient:
    def __init__(self, token: str):
        self.token = token
        self.client = 1


@app.task()
def sender(
        mail_id: str or int,
):
    client = telebot.TeleBot(token='6131419774:AAGDMNowAKTI_PbCU1KjM-DV65_M8k4lfkc', parse_mode='HTML')
    client.send_message(
        chat_id=572982939,
        text='Хуй'
    )
    mail: MailingModel = MailingModel.objects.get(id=mail_id)
    bot: BotModel = mail.bot
    bot_token: str = bot.id_bot
    user_list: UserModel = UserModel.objects.filter(bot=bot).values('telegram_id')
    client = telebot.TeleBot(token=bot_token, parse_mode='HTML')

    MailingModel.objects.filter(id=mail_id).update(
        status_send='В процессе',
        count_to_mailing=len(user_list)
    )
    sender_master(
        client=client,
        user_list=user_list,
        photo=mail.image.url,
        text=mail.text,
    )