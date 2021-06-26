from .bot_steps import *
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
from .models import Client
from .bot import send_message
from language.lang import get_all_langs


def get_message(update):
    if "text" in update["message"]:
        return update["message"]["text"]
    else:
        return None


def get_or_create_client(user_id):
    client = Client.objects.filter(user_id=user_id)
    if client.exists():
        return client.first()
    else:
        client = Client()
        client.user_id = user_id
        client.bot_step = MAIN_MENU
        client.save()
        return client


def get_lang(user_id):
    client = get_or_create_client(user_id)

    if client:
        return get_all_langs(client)
    else:
        client = get_or_create_client(user_id)
        return get_all_langs(client)


def get_client_first_name(user_id):
    client = get_or_create_client(user_id)
    return client.first_name


def get_client_last_name(user_id):
    client = get_or_create_client(user_id)
    return client.last_name


def get_client_middle_name(user_id):
    client = get_or_create_client(user_id)
    return client.middle_name


def get_client_bot_step(user_id):
    client = get_or_create_client(user_id)
    return client.bot_step


@csrf_exempt
def main(request):
    update = json.loads(request.body)
    user_id = update["message"]["from"]["id"]

    message = get_message(update)
    LANG_LIST = get_lang(user_id)
    client = get_or_create_client(user_id)

    if not message:
        return

    if not get_client_first_name(user_id).strip() and get_client_bot_step(user_id) == MAIN_MENU:
        client.bot_step = ASK_FULLNAME
        client.save()
        send_message(LANG_LIST[1], 810916014)

    elif get_client_bot_step(user_id) == ASK_FULLNAME:
        client.first_name = message
        client.save()
    
    return HttpResponse(update["message"]["text"])