from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint

@csrf_exempt
def main(request):
    update = json.loads(request.body)
    
    message = update["message"]["text"]
    user_id = update["message"]["from"]["id"]
    
    return HttpResponse(update["message"]["text"])