from django.conf import settings
import requests as r


BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)


def bot(method, data):
    response = r.post(BASE_URL + method, json=data)
    return response


def send_message(text, chat_id, menu = None, parse_mode = "html"):
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}

    if menu:
        data["reply_markup"] = menu
    
    response = bot("sendMessage", data)
    return response


def delete_message(chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    return bot("deleteMessage", data)