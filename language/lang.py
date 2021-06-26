from .models import Language

def get_all_langs(client):
    if client.lang == "UZB":
        return list(map(lambda lang: lang.uzb, list(Language.objects.filter().order_by("id"))))
    elif client.lang == "RUS":
        return list(map(lambda lang: lang.rus, list(Language.objects.filter().order_by("id"))))
