from django.contrib import admin
from .models import *


class LanguageAdmin(admin.ModelAdmin):
    list_display = ["id", "uzb", "rus"]
    list_display_links = ["id", "uzb", "rus"]
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Language, LanguageAdmin)