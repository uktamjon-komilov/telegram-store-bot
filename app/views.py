from .keyboards import *
from .bot_steps import *
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .bot import send_message, send_photo, delete_message
from .helpers import *
from .inline_commands import *
from pprint import pprint


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


    if message == LANG_LIST[6] or message == "/start":
        client.bot_step = MAIN_MENU
        client.save()
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[28], user_id, menu)

    elif not get_client_fullname(user_id).strip() and get_client_bot_step(user_id) == MAIN_MENU:
        client.bot_step = ASK_FULLNAME
        client.save()
        send_message(LANG_LIST[1], 810916014)

    elif get_client_bot_step(user_id) == ASK_FULLNAME:
        client.fullname = message
        client.bot_step = ASK_PHONE
        client.save()
        menu = create_contact_keyboard(LANG_LIST[16])
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
        menu = create_category_button(user_id)
        send_message(LANG_LIST[5], user_id, menu)
    
    elif get_client_bot_step(user_id) == CHOOSE_CATEGORY:
        try:
            category = Category.objects.get(category_name=message)
            products = Product.objects.filter(category=category, is_active=True)
            if products.exists():
                menu = create_product_message(products, user_id, 0, 3)
                client.bot_step = CHOOSE_PRODUCT
                client.save()
                product_detail = get_product_detail(products, user_id, 0)
                send_message(product_detail, user_id, menu)
            else:
                client.bot_step = CHOOSE_CATEGORY
                client.save()
                send_message(LANG_LIST[29], user_id)
                menu = create_category_button(user_id)
                send_message(LANG_LIST[5], user_id, menu)

        except Exception as e:
            print(e)
            client.bot_step = CHOOSE_CATEGORY
            client.save()
            send_message(LANG_LIST[18], user_id)
    
    elif message == LANG_LIST[25]:
        client.bot_step = CHOOSE_CATEGORY
        client.save()
        menu = create_category_button(user_id)
        send_message(LANG_LIST[5], user_id, menu)
    
    elif isinstance(callback_data, str) and callback_data.split("-")[0] == ADD_CART:
        product_id = callback_data.split("-")[-1]
        product = Product.objects.filter(id=product_id)
        if product.exists():
            product = product.first()
        else:
            client.bot_step = CHOOSE_CATEGORY
            client.save()
            send_message(LANG_LIST[18], user_id)

        cart = Cart.objects.filter(client_user_id=user_id)
        if cart.exists():
            cart = cart.first()
        else:
            cart = Cart(client_user_id=user_id)
            cart.save()
        
        cartitem = CartItem.objects.filter(cart=cart, product=product)
        quantity = update["callback_query"]["message"]["reply_markup"]["inline_keyboard"][0][1]["text"]
        if cartitem.exists():
            cartitem = cartitem.first()
            cartitem.quantity = int(quantity)
            cartitem.save()
        else:
            cartitem = CartItem(cart=cart, product=product, quantity=quantity)
            cartitem.save()

        send_message("qoshildi", user_id)        
    
    else:
        client.bot_step = MAIN_MENU
        client.save()
        send_message(LANG_LIST[18], user_id)
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[28], user_id, menu)

    return HttpResponse("Salom")