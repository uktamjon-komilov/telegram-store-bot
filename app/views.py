from .keyboards import *
from .bot_steps import *
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
from .models import *
from .bot import send_message, delete_message
from .helpers import *


@csrf_exempt
def main(request):
    REGION_INLINE_KEYBOARD = create_regions_keyboard()

    update = json.loads(request.body)

    user_id = get_user_id(update)
    message = get_message(update)
    callback_message_id = get_callback_message_id(update)
    callback_text = get_callback_text(update)
    callback_data = get_callback_data(update)
    LANG_LIST = get_lang(user_id)
    client = get_or_create_client(user_id)

    if not get_client_fullname(user_id).strip() and get_client_bot_step(user_id) == MAIN_MENU:
        client.bot_step = ASK_FULLNAME
        client.save()
        send_message(LANG_LIST[1], 810916014)

    elif get_client_bot_step(user_id) == ASK_FULLNAME:
        client.fullname = message
        client.bot_step = ASK_PHONE
        client.save()
        menu = create_contact_button(LANG_LIST[16])
        send_message(LANG_LIST[2], 810916014, menu)
    
    elif get_client_bot_step(user_id) == ASK_PHONE:
        if get_phone(update):
            client.phone = get_phone(update)
        else:
            client.phone = message

        client.bot_step = ASK_REGION
        client.save()
        send_message(LANG_LIST[3], user_id, REGION_INLINE_KEYBOARD)
    
    elif callback_text == LANG_LIST[3] and get_client_bot_step(user_id) == ASK_REGION:
        menu = create_districts_keyboard(callback_data)
        client.bot_step = ASK_DISTRICT
        client.save()
        delete_message(user_id, callback_message_id)
        send_message(LANG_LIST[4], user_id, menu)
    
    elif callback_text == LANG_LIST[4] and get_client_bot_step(user_id) == ASK_DISTRICT:
        client.district = District.objects.get(id=callback_data)
        client.bot_step = CHOOSE_CATEGORY
        client.save()
        delete_message(user_id, callback_message_id)
        send_message(LANG_LIST[17], user_id)
        send_message(LANG_LIST[5], user_id)

    return HttpResponse("Salom")