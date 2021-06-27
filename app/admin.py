from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "description", "price", "category", "is_active")
    list_editable = ["is_active"]


class CategoryAdmin(admin.ModelAdmin):
    fields = ["category_name"]


class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "fullname", "district", "user_id", "phone"]
    list_display_links = ["id", "fullname", "district", "user_id", "phone"]
    search_fields = ["fullname", "district__district_name", "district__region__region_name", "user_id", "phone"]


class RegionAdmin(admin.ModelAdmin):
    list_display = ["id", "region_name"]
    list_display_links = ["region_name"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "district_name"]
    list_display_links = ["district_name"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)

admin.site.unregister(Group)