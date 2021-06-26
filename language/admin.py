from django.contrib import admin
from .models import *


class LanguageAdmin(admin.ModelAdmin):
    list_display = ["id", "uzb", "rus"]
    list_editable = ["rus"]

admin.site.register(Language)