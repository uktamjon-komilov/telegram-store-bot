from app.bot import send_photo
from django.db.models.base import Model
from django.db.models.enums import Choices
from django.db.models.fields import NullBooleanField
from .bot_steps import *
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import os
import uuid
from django.utils.html import mark_safe

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("images", filename)

from .managers import UserManager

from language.models import *


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    description = models.TextField(verbose_name="Mahsulot haqida", blank=True)
    price = models.FloatField(verbose_name="Narxi", default=0.0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, verbose_name="Kategoriyasi")
    is_active = models.BooleanField(verbose_name="Mavjudligi", default=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return f"{self.product_name} - {self.category}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(verbose_name="Mahsulat rasmi", upload_to=get_file_path, null=True, blank=True)


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="Username", max_length=13, blank=True, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


class Client(models.Model):
    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"

    fullname = models.CharField(verbose_name="To'liq ismi", max_length=255, blank=True)
    phone = models.CharField(verbose_name="Telefon raqami", max_length=15, null=True)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, verbose_name="Tumani", null=True)
    user_id = models.IntegerField(verbose_name="Telegram foydalanuvchi IDsi", default=0)

    STEPS = [
        (MAIN_MENU, MAIN_MENU),
        (ASK_FULLNAME, ASK_FULLNAME),
        (ASK_PHONE, ASK_PHONE),
        (ASK_REGION, ASK_REGION),
        (ASK_DISTRICT, ASK_DISTRICT),
        (CHOOSE_CATEGORY, CHOOSE_CATEGORY),
        (CHOOSE_PRODUCT, CHOOSE_PRODUCT),
        (CART, CART),
        (PASSPORT_SERIES, PASSPORT_SERIES),
        (PASSPORT_NUMBER, PASSPORT_NUMBER),
        (CONFIRMATION, CONFIRMATION),
    ]

    bot_step = models.CharField("Foydalanuvchining botdagi bosqichi", max_length=255, choices=STEPS, default=MAIN_MENU, null=True)
    lang = models.CharField(verbose_name="Til", max_length=255, default="UZB", null=True)

    def __str__(self):
        return f"{self.user_id} - {self.fullname}"
    

    def get_full_address(self):
        return f"{self.district.district_name} - {self.district.region.region_name}"


class Cart(models.Model):
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    client_user_id = models.CharField(verbose_name="Mijozning telegram IDsi", max_length=255)
    passport_series = models.CharField(verbose_name="Pasport seriyasi", max_length=2, null=True, blank=True)
    passport_number = models.CharField(verbose_name="Pasport raqami", max_length=15, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Faol", default=True)
    is_ordered = models.BooleanField(verbose_name="Buyurtma qilingan", default=False, null=True)
    is_finished = models.BooleanField(verbose_name="Hal etilganligi", default=False, null=True)

    created_at = models.DateTimeField(verbose_name="Kiritildi", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="O'zgartirildi", auto_now=True, null=True)

    def __str__(self):
        client = Client.objects.filter(user_id=self.client_user_id)
        if client.exists():
            client = client.first()
            return client.fullname
        else:
            return self.client_user_id


class CartItem(models.Model):
    class Meta:
        verbose_name = "Buyurtma jihoz"
        verbose_name_plural = "Buyurtma jihozlar"

    product = models.ForeignKey(Product, verbose_name="Mahsulot", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Miqdori")
    is_active = models.BooleanField(verbose_name="Faol", default=True)
    is_ordered = models.BooleanField(verbose_name="Buyurtma qilingan", default=False, null=True)

    created_at = models.DateTimeField(verbose_name="Kiritildi", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="O'zgartirildi", auto_now=True, null=True)

    def __str__(self):
        client = Client.objects.filter(user_id=self.cart.client_user_id)
        if client.exists():
            client = client.first()
            return f"{self.product} - {self.quantity} - {client.fullname}"
        else:
            return f"{self.product} - {self.quantity}"



class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/post/", null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        self.clear_content()
        try:
            from app.bot import send_message
            import socket
            clients = Client.objects.all()
            for client in clients:
                if self.image:
                    image = "https://hamrox.uz/" + self.image.url
                    print(image)
                    res = send_photo(image, self.content, client.user_id)
                    print(res)
                else:
                    res = send_message(self.content, client.user_id)
                    print(res)
        except Exception as e:
            print(e)

    def clear_content(self):
        self.content = self.content.replace("<p>", "").replace("</p>", "").replace(' style=""', "").replace("<br>", chr(10))