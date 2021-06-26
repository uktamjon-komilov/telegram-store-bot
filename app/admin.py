from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "description", "price", "category", "is_active")
    list_editable = ["is_active"]

class CategoryAdmin(admin.ModelAdmin):
    fields = ["category_name"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)