from .keyboards import *
from .bot_steps import *
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
from .models import *
from .bot import send_message
from .helpers import *


@csrf_exempt
def main(request):
    REGION_INLINE_KEYBOARD = create_regions_keyboard()

    update = json.loads(request.body)

    user_id = get_user_id(update)
    message = get_message(update)
    callback_id = get_callback_id(update)
    callback_text = get_callback_text(update)
    callback_data = get_callback_data(update)
    LANG_LIST = get_lang(user_id)
    client = get_or_create_client(user_id)

    if message:
        if not get_client_fullname(user_id).strip() and get_client_bot_step(user_id) == MAIN_MENU:
            client.bot_step = ASK_FULLNAME
            client.save()
            send_message(LANG_LIST[1], 810916014)

        elif get_client_bot_step(user_id) == ASK_FULLNAME:
            client.fullname = message
            client.bot_step = ASK_PHONE
            client.save()
            send_message(LANG_LIST[2], 810916014)
        
        elif get_client_bot_step(user_id) == ASK_PHONE:
            if get_phone(update):
                client.phone = get_phone(update)
            else:
                client.phone = message

            client.bot_step = ASK_REGION
            client.save()
            send_message(LANG_LIST[3], user_id, REGION_INLINE_KEYBOARD)

    elif callback_id:
        if callback_text == LANG_LIST[3]:
            pass

    return HttpResponse("Salom")