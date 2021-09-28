from .keyboards import *
from .bot_steps import *
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .bot import *
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

        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[28], user_id, menu)
        client.bot_step = MAIN_MENU
        client.save()

    elif not get_client_fullname(user_id).strip() and get_client_bot_step(user_id) == MAIN_MENU:
        send_message(LANG_LIST[1], user_id)
        client.bot_step = ASK_FULLNAME
        client.save()

    elif get_client_bot_step(user_id) == ASK_FULLNAME:
        menu = create_contact_keyboard(LANG_LIST[16])
        send_message(LANG_LIST[2], user_id, menu)
        client.fullname = message
        client.bot_step = ASK_PHONE
        client.save()
    
    elif get_client_bot_step(user_id) == ASK_PHONE:
        send_message(LANG_LIST[3], user_id, REGION_INLINE_KEYBOARD)

        if get_phone(update):
            client.phone = get_phone(update)
        else:
            client.phone = message

        client.bot_step = ASK_REGION
        client.save()
    
    elif callback_text == LANG_LIST[3] and get_client_bot_step(user_id) == ASK_REGION:
        menu = create_districts_keyboard(callback_data)
        send_message(LANG_LIST[4], user_id, menu)
        client.bot_step = ASK_DISTRICT
        client.save()
        delete_message(user_id, callback_message_id)
    
    elif callback_text == LANG_LIST[4] and get_client_bot_step(user_id) == ASK_DISTRICT:
        send_message(LANG_LIST[17], user_id)
        client.district = District.objects.get(id=callback_data)
        client.bot_step = CHOOSE_CATEGORY
        client.save()
        delete_message(user_id, callback_message_id)
        menu = create_category_button(user_id)
        send_message(LANG_LIST[5], user_id, menu)
    
    elif get_client_bot_step(user_id) == CHOOSE_CATEGORY:
        try:
            category = Category.objects.get(category_name=message)
            products = Product.objects.prefetch_related("category").filter(category=category, is_active=True)
            if products.exists():
                cart = get_or_create_cart(user_id)
                cartitem = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(product=products.first(), cart=cart, is_active=True)
                if cartitem.exists():
                    menu = create_product_message(products, user_id, products.first().id, cartitem.first().quantity)
                else:
                    menu = create_product_message(products, user_id, products.first().id, 0)
                client.bot_step = CHOOSE_PRODUCT
                client.save()

                images = get_product_images(products.first())
                product_detail = get_product_detail(products, user_id, products.first().id)

                if images and len(images) >= 1:
                    send_photo(images[0], product_detail, user_id, menu)
                else:
                    send_message(product_detail, user_id, menu)

            else:
                send_message(LANG_LIST[29], user_id)
                client.bot_step = CHOOSE_CATEGORY
                client.save()
                menu = create_category_button(user_id)
                send_message(LANG_LIST[5], user_id, menu)

        except Exception as e:
            print(e)
            send_message(LANG_LIST[18], user_id)
            client.bot_step = CHOOSE_CATEGORY
            client.save()
    
    elif message == LANG_LIST[25]:
        menu = create_category_button(user_id)
        send_message(LANG_LIST[5], user_id, menu)
        client.bot_step = CHOOSE_CATEGORY
        client.save()
    
    elif isinstance(callback_data, str) and callback_data.split("-")[0] == ADD_CART:
        product = get_cart_product(callback_data, client, user_id)
        if not product:
            pass

        cart = get_or_create_cart(user_id)
        if not cart:
            pass
        
        cartitem = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(cart=cart, product=product)
        quantity = update["callback_query"]["message"]["reply_markup"]["inline_keyboard"][0][1]["text"]
        if cartitem.exists():
            cartitem = cartitem.first()
            cartitem.quantity = int(quantity)
            cartitem.save()
        else:
            cartitem = CartItem(cart=cart, product=product, quantity=quantity)
            cartitem.save()

    elif isinstance(callback_data, str) and callback_data.split("-")[0] == PLUS:
        menu = create_spinner_menu()
        edit_reply_markup(user_id, callback_message_id, menu)

        product = get_cart_product(callback_data, client, user_id)
        print(product)
        if not product:
            pass

        cart = get_or_create_cart(user_id)
        print(cart)
        if not cart:
            pass

        quantity = increment_cartitem_quantity(cart, product, update, 1)
        print(quantity)
        
        products = Product.objects.prefetch_related("category").filter(category=product.category, is_active=True)
        print(products)
        menu = create_product_message(products, user_id, product.id, quantity)
        print(menu)
        edit_reply_markup(user_id, callback_message_id, menu)

    elif isinstance(callback_data, str) and callback_data.split("-")[0] == MINUS:
        menu = create_spinner_menu()
        edit_reply_markup(user_id, callback_message_id, menu)
        
        product = get_cart_product(callback_data, client, user_id)
        if not product:
            pass

        cart = get_or_create_cart(user_id)
        if not cart:
            pass

        quantity = decrement_cartitem_quantity(cart, product, update, 1)
        
        products = Product.objects.prefetch_related("category").filter(category=product.category, is_active=True)
        menu = create_product_message(products, user_id, product.id, quantity)
        edit_reply_markup(user_id, callback_message_id, menu)
    
    elif isinstance(callback_data, str) and callback_data.split("-")[0] == NEXT:
        delete_message(user_id, callback_message_id)
        
        next_product_id = int(callback_data.split("-")[-1])
        next_product = Product.objects.prefetch_related("category").filter(id=next_product_id).first()
        cart = get_or_create_cart(user_id)
        products = Product.objects.prefetch_related("category").filter(category=next_product.category, is_active=True)
        cartitem = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(product=next_product, cart=cart, is_active=True)
        if cartitem.exists():
            menu = create_product_message(products, user_id, next_product_id, cartitem.first().quantity)
        else:
            menu = create_product_message(products, user_id, next_product_id, 1)

        client.bot_step = CHOOSE_PRODUCT
        client.save()

        images = get_product_images(products.filter(id=next_product_id).first())
        product_detail = get_product_detail(products, user_id, next_product_id)

        if images and len(images) >= 1:
            send_photo(images[0], product_detail, user_id, menu)
        else:
            send_message(product_detail, user_id, menu)

    elif isinstance(callback_data, str) and callback_data.split("-")[0] == PREV:
        delete_message(user_id, callback_message_id)

        prev_product_id = int(callback_data.split("-")[-1])
        prev_product = Product.objects.prefetch_related("category").filter(id=prev_product_id).last()
        cart = get_or_create_cart(user_id)
        products = Product.objects.prefetch_related("category").filter(category=prev_product.category, is_active=True)
        cartitem = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(product=prev_product, cart=cart, is_active=True)
        if cartitem.exists():
            menu = create_product_message(products, user_id, prev_product_id, cartitem.first().quantity)
        else:
            menu = create_product_message(products, user_id, prev_product_id, 1)

        client.bot_step = CHOOSE_PRODUCT
        client.save()

        product_detail = get_product_detail(products, user_id, prev_product_id)
        images = get_product_images(products.filter(id=prev_product_id).first())

        if images and len(images) >= 1:
            send_photo(images[0], product_detail, user_id, menu)
        else:
            send_message(product_detail, user_id, menu)
    
    elif (isinstance(callback_data, str) and callback_data == GO_TO_CART) or message == LANG_LIST[8]:
        cart = get_or_create_cart(user_id)
        cartitems = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(cart=cart, is_active=True)

        if callback_data == GO_TO_CART:
            delete_message(user_id, callback_message_id)
        
        client.bot_step = MAIN_MENU
        client.save()
        menu = create_mainmenu_keyboard(user_id)

        if cartitems.exists():
            try:
                result = send_message("Loading...", user_id, menu)
                delete_message(user_id, result["result"]["message_id"])

                menu = create_clearcart_keyboard(cart, user_id)
                cart_details = create_cart_detail(user_id, cartitems)
                send_message(cart_details, user_id, menu)
            except Exception as e:
                send_message(str(e), user_id)
        else:
            send_message(LANG_LIST[37], user_id, menu)
        
    elif (isinstance(callback_data, str) and callback_data == CLEAR_CART) or message == LANG_LIST[7]:
        delete_message(user_id, callback_message_id)

        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[27], user_id, menu)

        cart = Cart.objects.filter(client_user_id=user_id, is_active=True)
        if cart.exists():
            cart = cart.first()
            try:
                cartitems = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(cart=cart, is_active=True).update(is_active=False)
            except Exception as e:
                print(e)
            cart.is_active = False
            cart.save()
        
        client.bot_step = MAIN_MENU
        client.save()
    
    elif message == LANG_LIST[26]:
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[40], user_id, menu)
        client.bot_step = MAIN_MENU
        client.save()
    
    elif isinstance(callback_data, str) and callback_data.split("-")[0] == ORDERING:
        cart_id = int(callback_data.split("-")[-1])
        cart = Cart.objects.filter(id=cart_id, is_active=True)
        if cart.exists():
            cart = cart.first()
            cartitems = CartItem.objects.prefetch_related("product").prefetch_related("cart").filter(cart=cart, is_active=True)
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
            menu = create_defaultmenu_keyboard(user_id)
            send_message(LANG_LIST[11], user_id, menu)
            cart.passport_series = message
            cart.save()
            client.bot_step = PASSPORT_NUMBER
            client.save()
        except:
            send_message(LANG_LIST[10], user_id, menu)
            menu = create_defaultmenu_keyboard(user_id)

    elif get_client_bot_step(user_id) == PASSPORT_NUMBER:
        cart = get_or_create_cart(user_id)
        try:
            menu = create_mainmenu_keyboard(user_id)
            send_message(LANG_LIST[14], user_id, menu)
            cart.passport_number = message
            cart.save()
            client.bot_step = MAIN_MENU
            client.save()
            cart.is_active = False
            cart.is_ordered = True
            cart.save()
        except:
            menu = create_defaultmenu_keyboard(user_id)
            send_message(LANG_LIST[10], user_id, menu)

    elif message == LANG_LIST[42]:
        menu = create_lang_keyboard(user_id)
        send_message(LANG_LIST[45], user_id, menu)
    
    elif message == LANG_LIST[43]:
        client.lang = "UZB"
        client.save()
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[46], user_id, menu)

    elif message == LANG_LIST[44]:
        client.lang = "RUS"
        client.save()
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[46], user_id, menu)

    else:
        client.bot_step = MAIN_MENU
        client.save()
        send_message(LANG_LIST[18], user_id)
        menu = create_mainmenu_keyboard(user_id)
        send_message(LANG_LIST[28], user_id, menu)

    return HttpResponse("Salom")


def stats(request):
    context = {
        "clients": Client.objects.all()
    }
    return render(request, "stats.html", context)


def ordered_products(request):
    ordered_products_list = []
    products = Product.objects.all()
    for product in products:
        cartitems = CartItem.objects.prefetch_related("product").filter(product=product)
        if cartitems.exists():
            ordered_products_list.append({"x": product.product_name, "y": 0})
            for cartitem in cartitems:
                ordered_products_list[-1]["y"] += cartitem.quantity
            
    return JsonResponse(ordered_products_list, safe=False)


def ordering_regions(request):
    ordering_regions_list = []
    regions = Region.objects.all()
    for region in regions:
        region_item = {"x": region.region_name, "y": 0}
        clients = list(map(lambda c: c.user_id, Client.objects.filter(district__region=region)))
        cartitems = CartItem.objects.filter(cart__client_user_id__in=clients)
        for cartitem in cartitems:
            region_item["y"] += cartitem.quantity
        
        ordering_regions_list.append(region_item)
    
    return JsonResponse(ordering_regions_list, safe=False)


def types_of_orders(request):
    active_orders = Cart.objects.filter(is_active=True)
    ordered_orders = Cart.objects.filter(is_ordered=True)
    finished_orders = Cart.objects.filter(is_finished=True)

    order_types = [
        {"x": "Yakunlanmagan buyurtmalar", "y": active_orders.count()},
        {"x": "Hal qilinmagan buyurtmalar", "y": ordered_orders.count()},
        {"x": "Hal qilingan buyurtmalar", "y": finished_orders.count()},
    ]

    return JsonResponse(order_types, safe=False)