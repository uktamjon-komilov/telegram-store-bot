from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *
from language.models import *


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


class CartItemAdmin(admin.ModelAdmin):
    # list_display = ["id", "product", "cart", "quantity"]
    pass

class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem
    exclude = ["is_active", "is_ordered"]

    def get_extra(self, request, obj=None, **kwargs):
        return 0


class CartAdmin(admin.ModelAdmin):
    def get_client(self, obj):
        client = Client.objects.filter(user_id=obj.client_user_id)
        if client.exists():
            client = client.first()
            return client.fullname
    get_client.short_description = 'Mijoz'
    get_client.admin_order_field = 'cart__client'

    def get_client_contact(self, obj):
        client = Client.objects.filter(user_id=obj.client_user_id)
        if client.exists():
            client = client.first()
            return client.phone
    get_client_contact.short_description = 'Telegfon raqami'
    get_client_contact.admin_order_field = 'cart__phone'

    def get_update_field(self, obj):
        return obj.updated_at.strftime("%Y.%m.%d, %H:%M")
    get_update_field.short_description = "O'zgartirilgan vaqti"
    get_update_field.admin_order_field = "cart__update_at"


    def get_created_field(self, obj):
        return obj.created_at.strftime("%Y.%m.%d, %H:%M")
    get_created_field.short_description = "Kiritilgan vaqti"
    get_created_field.admin_order_field = "cart__created_at"


    fields = ["client_user_id", "passport_series", "passport_number", "is_active", "is_ordered"]
    list_display = ["id", "get_client", "get_client_contact", "get_created_field", "get_update_field",  "is_ordered", "is_finished"]
    list_editable = ["is_finished"]
    list_display_links = ["id", "get_client", "get_client_contact"]
    inlines = [CartItemInlineAdmin]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)

admin.site.unregister(Group)