from .models import Region, District
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



def create_districts_keyboard(region):
    DISTRICTS_INLINE_KEYBOARD = {
        "inline_keyboard": []
    }

    districts = District.objects.filter(region=region)
    if districts.exists():
        districts = districts.order_by("district_name")
        for district in districts:
            DISTRICTS_INLINE_KEYBOARD["inline_keyboard"].append([{"text": district.district_name, "callback_data": district.id}])
    else:
        return None
    
    return DISTRICTS_INLINE_KEYBOARD