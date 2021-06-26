from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint
from .models import Client

@csrf_exempt
def main(request):
    update = json.loads(request.body)
    
    message = update["message"]["text"]
    user_id = update["message"]["from"]["id"]

    if message == "/start":
        client = Client.objects.filter(user__username=str(user_id))
        if client.exists():
            pass
    
    return HttpResponse(update["message"]["text"])