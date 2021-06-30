from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.contrib import admin

admin.site.site_header = "Telegram Bot Administratsiyasi"
admin.site.site_title = "Administrativ Portal"
admin.site.index_title = "Telegram Bot Administratsiyasi"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
