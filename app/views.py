from .keyboards import *
from .bot_steps import *
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .bot import send_message, send_photo_group, edit_message, delete_message
from .helpers import *
from .inline_commands import *
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse


@csrf_exempt
def main(request):
    REGION_INLINE_KEYBOARD = create_regions_keyboard()

    if request.method == "GET":
        return HttpResponse("Salom")

    update = json.loads(request.body)

    user_id = get_user_id(update)
    message = get_message(update)
    message_id = get_message_id(update)
    callback_message_id = get_callback_message_id(update)
    callback_text = get_callback_text(update)
    callback_data = get_callback_data(update)
    LANG_LIST = get_lang(user_id)
    client = get_or_create_client(user_id)


    if message == LANG_LIST[6] or message == "/start" or callback_data == MAIN_MENU_INLINE:
        if callback_data == MAIN_MENU_INLINE:
            delete_message(user_id, callback_message_id)

        client.bot_step = MAIN_MENU
        client.save()
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[28], user_id, menu)

    elif not get_client_fullname(user_id).strip() and get_client_bot_step(user_id) == MAIN_MENU:
        client.bot_step = ASK_FULLNAME
        client.save()
        send_message(LANG_LIST[1], user_id)

    elif get_client_bot_step(user_id) == ASK_FULLNAME:
        client.fullname = message
        client.bot_step = ASK_PHONE
        client.save()
        menu = create_contact_keyboard(LANG_LIST[16])
        send_message(LANG_LIST[2], user_id, menu)
    
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
                cart = get_or_create_cart(user_id)
                cartitem = CartItem.objects.filter(product=products.first(), cart=cart, is_active=True)
                if cartitem.exists():
                    menu = create_product_message(products, user_id, products.first().id, cartitem.first().quantity)
                else:
                    menu = create_product_message(products, user_id, products.first().id, 0)
                client.bot_step = CHOOSE_PRODUCT
                client.save()

                images = get_product_images(products.first())
                if images:
                    print(images)
                    print(send_photo_group(images, user_id))
                product_detail = get_product_detail(products, user_id, products.first().id)
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
        product = get_cart_product(callback_data, client, user_id)
        if not product:
            pass

        cart = get_or_create_cart(user_id)
        if not cart:
            pass
        
        cartitem = CartItem.objects.filter(cart=cart, product=product)
        quantity = update["callback_query"]["message"]["reply_markup"]["inline_keyboard"][0][1]["text"]
        if cartitem.exists():
            cartitem = cartitem.first()
            cartitem.quantity = int(quantity)
            cartitem.save()
        else:
            cartitem = CartItem(cart=cart, product=product, quantity=quantity)
            cartitem.save()

    elif isinstance(callback_data, str) and callback_data.split("-")[0] == PLUS:
        product = get_cart_product(callback_data, client, user_id)
        if not product:
            pass

        cart = get_or_create_cart(user_id)
        if not cart:
            pass

        quantity = increment_cartitem_quantity(cart, product, update, 1)
        
        products = Product.objects.filter(category=product.category, is_active=True)
        menu = create_product_message(products, user_id, product.id, quantity)
        product_detail = get_product_detail(products, user_id, product.id, LANG_LIST[35])
        edit_message(product_detail, user_id, callback_message_id, menu)

    elif isinstance(callback_data, str) and callback_data.split("-")[0] == MINUS:
        product = get_cart_product(callback_data, client, user_id)
        if not product:
            pass

        cart = get_or_create_cart(user_id)
        if not cart:
            pass

        quantity = decrement_cartitem_quantity(cart, product, update, 1)
        
        products = Product.objects.filter(category=product.category, is_active=True)
        menu = create_product_message(products, user_id, product.id, quantity)
        product_detail = get_product_detail(products, user_id, product.id, LANG_LIST[36])
        edit_message(product_detail, user_id, callback_message_id, menu)
    
    elif isinstance(callback_data, str) and callback_data.split("-")[0] == NEXT:
        next_product_id = int(callback_data.split("-")[-1])
        next_product = Product.objects.filter(id=next_product_id).first()
        cart = get_or_create_cart(user_id)
        products = Product.objects.filter(category=next_product.category, is_active=True)
        cartitem = CartItem.objects.filter(product=next_product, cart=cart, is_active=True)
        if cartitem.exists():
            menu = create_product_message(products, user_id, next_product_id, cartitem.first().quantity)
        else:
            menu = create_product_message(products, user_id, next_product_id, 1)

        client.bot_step = CHOOSE_PRODUCT
        client.save()
        product_detail = get_product_detail(products, user_id, next_product_id)
        edit_message(product_detail, user_id, callback_message_id, menu)

    elif isinstance(callback_data, str) and callback_data.split("-")[0] == PREV:
        prev_product_id = int(callback_data.split("-")[-1])
        prev_product = Product.objects.filter(id=prev_product_id).last()
        cart = get_or_create_cart(user_id)
        products = Product.objects.filter(category=prev_product.category, is_active=True)
        cartitem = CartItem.objects.filter(product=prev_product, cart=cart, is_active=True)
        if cartitem.exists():
            menu = create_product_message(products, user_id, prev_product_id, cartitem.first().quantity)
        else:
            menu = create_product_message(products, user_id, prev_product_id, 1)

        client.bot_step = CHOOSE_PRODUCT
        client.save()
        product_detail = get_product_detail(products, user_id, prev_product_id)
        edit_message(product_detail, user_id, callback_message_id, menu)
    
    elif (isinstance(callback_data, str) and callback_data == GO_TO_CART) or message == LANG_LIST[8]:
        cart = get_or_create_cart(user_id)
        cartitems = CartItem.objects.filter(cart=cart, is_active=True)

        if callback_data == GO_TO_CART:
            delete_message(user_id, callback_message_id)
        
        client.bot_step = MAIN_MENU
        client.save()
        menu = create_mainmenu_keyboard(user_id)

        if cartitems.exists():
            result = send_message("Loading...", user_id, menu)
            delete_message(user_id, result["result"]["message_id"])

            menu = create_clearcart_keyboard(cart, user_id)
            cart_details = create_cart_detail(user_id, cartitems)
            send_message(cart_details, user_id, menu)
        else:
            send_message(LANG_LIST[37], user_id, menu)
        
    elif (isinstance(callback_data, str) and callback_data == CLEAR_CART) or message == LANG_LIST[7]:
        cart = Cart.objects.filter(client_user_id=user_id, is_active=True)
        if cart.exists():
            cart = cart.first()
            try:
                cartitems = CartItem.objects.filter(cart=cart, is_active=True).update(is_active=False)
            except Exception as e:
                print(e)
            cart.is_active = False
            cart.save()
        
        delete_message(user_id, callback_message_id)
        client.bot_step = MAIN_MENU
        client.save()
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[27], user_id, menu)
    
    elif message == LANG_LIST[26]:
        client.bot_step = MAIN_MENU
        client.save()
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[40], user_id, menu)
    
    elif isinstance(callback_data, str) and callback_data.split("-")[0] == ORDERING:
        cart_id = int(callback_data.split("-")[-1])
        cart = Cart.objects.filter(id=cart_id, is_active=True)
        if cart.exists():
            cart = cart.first()
            cartitems = CartItem.objects.filter(cart=cart, is_active=True)
            if cartitems.exists():
                for cartitem in cartitems:
                    cartitem.is_ordered = True
                    cartitem.is_active = False
                    cartitem.save()
                
                cart.save()

                delete_message(user_id, callback_message_id)
                client.bot_step = PASSPORT_SERIES
                client.save()
                menu = create_defaultmenu_keyboard(user_id)
                send_message(LANG_LIST[9], user_id, menu)
                send_message(LANG_LIST[10], user_id, menu)
                
            else:
                delete_message(user_id, callback_message_id)
                client.bot_step = MAIN_MENU
                client.save()
                menu = create_mainmenu_keyboard(user_id)
                send_message(LANG_LIST[37], user_id, menu)
    
    elif get_client_bot_step(user_id) == PASSPORT_SERIES:
        cart = get_or_create_cart(user_id)
        try:
            cart.passport_series = message
            cart.save()
            menu = create_defaultmenu_keyboard(user_id)
            client.bot_step = PASSPORT_NUMBER
            client.save()
            send_message(LANG_LIST[11], user_id, menu)
        except:
            menu = create_defaultmenu_keyboard(user_id)
            send_message(LANG_LIST[10], user_id, menu)

    elif get_client_bot_step(user_id) == PASSPORT_NUMBER:
        cart = get_or_create_cart(user_id)
        try:
            cart.passport_number = message
            cart.save()
            client.bot_step = MAIN_MENU
            cart.is_active = False
            cart.is_ordered = True
            client.save()
            menu = create_mainmenu_keyboard(user_id)
            send_message(LANG_LIST[14], user_id, menu)
        except:
            menu = create_defaultmenu_keyboard(user_id)
            send_message(LANG_LIST[10], user_id, menu)

    else:
        client.bot_step = MAIN_MENU
        client.save()
        send_message(LANG_LIST[18], user_id)
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[28], user_id, menu)

    return HttpResponse("Salom")


def stats(request):
    return render(request, "stats.html")


def pivot_data(request):
    dataset = CartItem.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)