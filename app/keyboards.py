from typing import Text
from language.models import Language
from .models import *
from .helpers import get_lang
from .inline_commands import *
from pprint import pprint

def create_regions_keyboard():
    REGIONS_INLINE_KEYBOARD = {
        "inline_keyboard": []
    }

    regions = Region.objects.filter()
    if regions.exists():
        regions = regions.order_by("region_name")
        for region in regions:
            REGIONS_INLINE_KEYBOARD["inline_keyboard"].append([{"text": region.region_name, "callback_data": region.id}])
    else:
        return None

    return REGIONS_INLINE_KEYBOARD

def create_districts_keyboard(region_id):
    DISTRICTS_INLINE_KEYBOARD = {
        "inline_keyboard": []
    }

    region = Region.objects.filter(id=int(region_id))
    if not region.exists():
        return None
    else:
        region = region.first()

    districts = District.objects.filter(region=region)
    if districts.exists():
        districts = districts.order_by("district_name")
        for district in districts:
            DISTRICTS_INLINE_KEYBOARD["inline_keyboard"].append([{"text": district.district_name, "callback_data": district.id}])
    else:
        return None
    
    return DISTRICTS_INLINE_KEYBOARD


def create_contact_keyboard(text):
    CONTACT_BUTTON = {
        "keyboard": [
            [{"text": text, "request_contact": True}]
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True
    }

    return CONTACT_BUTTON


def create_category_button(user_id):
    LANG_LIST = get_lang(user_id)
    CATEGORY_KEYBOARD = {
        "keyboard": [
            [{"text": LANG_LIST[6]}, {"text": LANG_LIST[7]}],
            [],
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True
    }
    categories = Category.objects.filter()
    if categories.exists():
        categories = categories.order_by("-id")
        for cat in categories:
            if len(CATEGORY_KEYBOARD["keyboard"][-1]) == 2:
                CATEGORY_KEYBOARD["keyboard"].append([])
            CATEGORY_KEYBOARD["keyboard"][-1].append({"text": cat.category_name})
        
        return CATEGORY_KEYBOARD
    
    return None


def create_product_message(products, user_id, id=0, quanity=1):
    if products.exists():
        products = products.order_by("id")
        product = list(filter(lambda product: product.id == id, list(products)))[0]
        LANG_LIST = get_lang(user_id)
        PRODUCT_INLINE_KEYBOARD = {
            "inline_keyboard": [
                [
                    {"text": LANG_LIST[20], "callback_data": f"{MINUS}-{product.id}"},
                    {"text": quanity, "callback_data": NONE},
                    {"text": LANG_LIST[19], "callback_data": f"{PLUS}-{product.id}"}
                ],
                [
                    {"text": LANG_LIST[21], "callback_data": f"{ADD_CART}-{product.id}"}
                ],
                [
                    {"text": LANG_LIST[24], "callback_data": GO_TO_CART}
                ],
                [
                    {"text": LANG_LIST[6], "callback_data": MAIN_MENU_INLINE},
                    {"text": LANG_LIST[7], "callback_data": CLEAR_CART}
                ],
            ]
        }

        prev_products = list(filter(lambda product: product.id < id, list(products)))
        if len(prev_products):
            last_prev_product = prev_products[-1]
            PRODUCT_INLINE_KEYBOARD["inline_keyboard"][1].insert(0, {"text": LANG_LIST[22], "callback_data": f"{PREV}-{last_prev_product.id}"})
        
        next_products = list(filter(lambda product: product.id > id, list(products)))
        if len(next_products):
            first_next_product = next_products[0]
            PRODUCT_INLINE_KEYBOARD["inline_keyboard"][1].append({"text": LANG_LIST[23], "callback_data": f"{NEXT}-{first_next_product.id}"})
        
        return PRODUCT_INLINE_KEYBOARD

    else:
        return None


def create_mainmenu_keyboard(user_id):
    LANG_LIST = get_lang(user_id)
    MAIN_MENU_KEYBOARD = {
        "keyboard": [
            [
                {"text": LANG_LIST[25]},
                {"text": LANG_LIST[8]}
            ],
            [
                {"text": LANG_LIST[26]},
                {"text": LANG_LIST[7]},
            ]
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True
    }

    return MAIN_MENU_KEYBOARD


def get_product_detail(products, user_id, id=0, extra_text=""):
    LANG_LIST = get_lang(user_id)

    text = ""

    product = list(filter(lambda product: product.id == id, list(products)))[0]

    text += (LANG_LIST[30] + " " + product.product_name + "\n")
    text += (LANG_LIST[31] + " " + str(product.price) + "\n")
    text += (LANG_LIST[32] + " " + product.category.category_name + "\n")
    if product.description:
        text += (LANG_LIST[33] + " " + product.description + "\n")
    
    if extra_text:
        text += ("\n" + extra_text)

    return text


def create_clearcart_keyboard(cart, user_id):
    LANG_LIST = get_lang(user_id)
    CART_INLINE_KEYBOARD = {
        "inline_keyboard": [
            [
                {"text": LANG_LIST[7], "callback_data": CLEAR_CART},
                {"text": LANG_LIST[39], "callback_data": f"{ORDERING}-{cart.id}"},
            ],
            [
                {"text": LANG_LIST[6], "callback_data": MAIN_MENU_INLINE},
            ],
        ]
    }

    return CART_INLINE_KEYBOARD


def create_defaultmenu_keyboard(user_id):
    LANG_LIST = get_lang(user_id)
    DEFAULT_KEYBOARD = {
        "keyboard": [
            [
                {"text": LANG_LIST[6]},
                {"text": LANG_LIST[7]}
            ]
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True
    }

    return DEFAULT_KEYBOARD