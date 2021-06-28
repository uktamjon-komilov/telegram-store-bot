from django.conf import settings
from django.http import response
import requests as r


BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)


def bot(method, data):
    response = r.post(BASE_URL + method, json=data)
    return response


def send_message(text, chat_id, menu = None, parse_mode = "html"):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }

    if menu:
        data["reply_markup"] = menu
    
    return bot("sendMessage", data)


def send_photo(photo_url, chat_id, menu, parse_mode="html"):
    data = {
        "chat_id": chat_id,
        "photo": photo_url,
        "parse_mode": parse_mode
    }

    if menu:
        data["reply_markup"] = menu

    return bot("sendPhoto", data)


def edit_message(text, chat_id, message_id, menu = None, parse_mode = "html"):
    data = {
        "chat_id": chat_id,
        "text": text,
        "message_id": message_id,
        "parse_mode": parse_mode
    }

    if menu:
        data["reply_markup"] = menu
    
    return bot("editMessageText", data)


def delete_message(chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    return bot("deleteMessage", data)