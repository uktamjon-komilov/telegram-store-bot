from django.db.models.enums import Choices
from .bot_steps import *
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


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


class Region(models.Model):
    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
    
    region_name = models.CharField(verbose_name="Viloyat nomi", max_length=255)

    def __str__(self):
        return self.region_name


class District(models.Model):
    class Meta:
        verbose_name = "Tuman/Shahar"
        verbose_name_plural = "Tumanlar/Shaharlar"

    district_name = models.CharField(verbose_name="Tuman/shahar nomi", max_length=255)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.district_name} - {self.region}"


class Client(models.Model):
    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"

    first_name = models.CharField(verbose_name="Ismi", max_length=255, blank=True)
    last_name = models.CharField(verbose_name="Familiyasi", max_length=255, blank=True)
    middle_name = models.CharField(verbose_name="Otasining ismi", max_length=255, blank=True)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, verbose_name="Tumani")
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
        (MAKE_CONTRACT, MAKE_CONTRACT),
        (PASSPORT_SERIES, PASSPORT_SERIES),
        (PASSPORT_NUMBER, PASSPORT_NUMBER),
        (CONFIRMATION, CONFIRMATION),
    ]

    bot_step = models.CharField("Foydalanuvchining botdagi bosqichi", max_length=255, choices=STEPS, default=MAIN_MENU, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.first_name}"