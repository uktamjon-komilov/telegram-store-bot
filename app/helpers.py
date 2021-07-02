from app.utils import truncate
from language.models import Language
from .models import Client
from .bot_steps import *
from language.lang import get_all_langs
from .bot import send_message
from .models import *

def get_message(update):
    if not "message" in update:
        return None

    if "text" in update["message"]:
        return update["message"]["text"]
    else:
        return None

def get_message_id(update):
    if not "message" in update:
        return None

    if "text" in update["message"]:
        return update["message"]["message_id"]
    else:
        return None

def get_phone(update):
    if "contact" in update["message"]:
        return update["message"]["contact"]["phone_number"]
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


def get_client_fullname(user_id):
    client = get_or_create_client(user_id)
    return client.fullname


def get_client_bot_step(user_id):
    client = get_or_create_client(user_id)
    return client.bot_step


def get_user_id(update):
    if "message" in update:
        return update["message"]["from"]["id"]
    elif "callback_query" in update:
        return update["callback_query"]["from"]["id"]


def get_callback_message_id(update):
    if "callback_query" in update:
        return update["callback_query"]["message"]["message_id"]
    else:
        return None

def get_callback_text(update):
    if "callback_query" in update:
        if "text" in update["callback_query"]["message"]:
            return update["callback_query"]["message"]["text"]
        else:
            return None
    else:
        return None


def get_callback_data(update):
    if "callback_query" in update:
        return update["callback_query"]["data"]
    else:
        return None


def get_cart_product(callback_data, client, user_id):
    product_id = callback_data.split("-")[-1]
    product = Product.objects.filter(id=product_id)
    if product.exists():
        product = product.first()
        return product
    else:
        client.bot_step = CHOOSE_CATEGORY
        client.save()
        LANG_LIST = get_lang(user_id)
        send_message(LANG_LIST[18], user_id)
        return None


def get_or_create_cart(user_id):
    cart = Cart.objects.filter(client_user_id=user_id, is_active=True, is_ordered=False)
    if cart.exists():
        cart = cart.first()
    else:
        cart = Cart(client_user_id=user_id)
        cart.save()
    
    return cart


def increment_cartitem_quantity(cart, product, update, amount):
    cartitem = CartItem.objects.filter(cart=cart, product=product)
    quantity = update["callback_query"]["message"]["reply_markup"]["inline_keyboard"][0][1]["text"]
    quantity = int(quantity)
    if cartitem.exists():
        cartitem = cartitem.first()
        quantity += amount
        cartitem.quantity = quantity
        cartitem.save()
    else:
        cartitem = CartItem(cart=cart, product=product, quantity=quantity)
        cartitem.save()
    
    return quantity


def decrement_cartitem_quantity(cart, product, update, amount):
    cartitem = CartItem.objects.filter(cart=cart, product=product)
    quantity = update["callback_query"]["message"]["reply_markup"]["inline_keyboard"][0][1]["text"]
    quantity = int(quantity)
    if cartitem.exists():
        cartitem = cartitem.first()
        if quantity > 0:
            quantity -= amount
        cartitem.quantity = quantity
        cartitem.save()
    else:
        cartitem = CartItem(cart=cart, product=product, quantity=quantity)
        cartitem.save()
    
    return quantity


def create_cart_detail(user_id, cartitems):
    LANG_LIST = get_lang(user_id)
    text = ""

    text += (LANG_LIST[38] + "\n\n")

    for cartitem in cartitems:
        text += (LANG_LIST[30] + " " + cartitem.product.product_name + "\n")
        text += (LANG_LIST[41] + " " + str(cartitem.quantity) + "\n")
        text += (LANG_LIST[31] + " " + str(cartitem.product.price) + "x" + str(cartitem.quantity) + "=" + str(cartitem.product.price*cartitem.quantity) + "\n")
        text += (LANG_LIST[32] + " " + cartitem.product.category.category_name + "\n")
        if cartitem.product.description:
            text += (LANG_LIST[33] + " " + truncate(cartitem.product.description, 50) + "\n")
        text += "\n"

    return text


def get_product_images(product):
    images = ProductImage.objects.filter(product=product)
    image_urls = []
    if images.exists():
        for image in images:
            image_urls.append("https://hamrox.uz/" + image.image.url)
        return image_urls
    else:
        return None