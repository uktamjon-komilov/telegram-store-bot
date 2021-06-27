from typing import Text
from language.models import Language
from .models import Region, District, Category
from .helpers import get_lang
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
            [{"text": LANG_LIST[6]}, {"text": LANG_LIST[27]}],
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


def create_product_message(products, user_id, index=0, quanity=1):
    if products.exists():
        products = list(products)
        product = products[index]
        LANG_LIST = get_lang(user_id)
        PRODUCT_INLINE_KEYBOARD = {
            "inline_keyboard": [
                [
                    {"text": LANG_LIST[20], "callback_data": f"plus-{product.id}"},
                    {"text": quanity, "callback_data": "None"},
                    {"text": LANG_LIST[19], "callback_data": f"minus-{product.id}"}
                ],
                [
                    {"text": LANG_LIST[21], "callback_data": f"add_cart-{product.id}"}
                ],
                [
                    {"text": LANG_LIST[24], "callback_data": "go_to_cart"}
                ]
            ]
        }

        if index != 0:
            PRODUCT_INLINE_KEYBOARD["inline_keyboard"][1].insert(0, {"text": LANG_LIST[22], "callback_data": f"prev-{index-1}"})
        
        if len(products)-1 > index:
            PRODUCT_INLINE_KEYBOARD["inline_keyboard"][1].append({"text": LANG_LIST[23], "callback_data": f"next-{index+1}"})
        
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
                {"text": LANG_LIST[27]},
            ]
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True
    }

    return MAIN_MENU_KEYBOARD