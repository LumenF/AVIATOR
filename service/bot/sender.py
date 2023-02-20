import os

from telebot import TeleBot

from AVIATOR.settings import MEDIA_PATH


def send_text(
        client: TeleBot,
        user_id: str,
        text: str,
) -> True or False:
    try:
        client.send_message(
            chat_id=user_id,
            text=text
        )
        return True
    except:
        return False


def send_text_and_photo(
        client: TeleBot,
        user_id: str,
        text: str,
        photo,
) -> True or False:
    try:
        client.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=text,
        )
        return True
    except:
        return False


def sender_master(
        client: TeleBot,
        user_list: list,
        photo: str,
        text: str,
):
    mail_success = 0
    user_success = []

    mail_fail = 0
    users_fail = []

    if text and not photo:
        for user in user_list:
            result = send_text(
                client=client,
                user_id=user['telegram_id'],
                text=text
            )
            if result:
                mail_success += 1
                user_success.append(user['telegram_id'])
            else:
                mail_fail += 1
                users_fail.append(user['telegram_id'])
        return
    if text and photo:
        image_check = os.path.exists(MEDIA_PATH + photo.replace('/', r'\\'))
        if not image_check:
            return 500

        with open(MEDIA_PATH + photo.replace('/', r'\\'), 'rb') as image_file:
            for user in user_list:
                result = send_text_and_photo(
                    client=client,
                    user_id=user['telegram_id'],
                    photo=image_file,
                    text=text
                )
                if result:
                    mail_success += 1
                    user_success.append(user['telegram_id'])
                else:
                    mail_fail += 1
                    users_fail.append(user['telegram_id'])
            return
