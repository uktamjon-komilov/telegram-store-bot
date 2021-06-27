from .models import Region, District, Category
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


def create_category_button():
    CATEGORY_KEYBOARD = {
        "keyboard": [[]],
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


# def create_product_message(products, index=1):
#     PRODU