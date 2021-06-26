from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Telefon raqam kiritilishi shart")
        user = self.model(phone = phone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, phone, password):
        user = self.create_user(phone, password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(verbose_name="Ismi", max_length=255, blank=True)
    last_name = models.CharField(verbose_name="Familiyasi", max_length=255, blank=True)
    middle_name = models.CharField(verbose_name="Otasining ismi", max_length=255, blank=True)
    phone = models.CharField(verbose_name="Telefon raqami", max_length=13, blank=True, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} - {self.phone}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


class Region(models.Model):
    region_name = models.CharField(verbose_name="Viloyat nomi", max_length=255)

    def __str__(self):
        return self.region_name


class District(models.Model):
    district_name = models.CharField(verbose_name="Tuman/shahar nomi", max_length=255)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.district_name} - {self.region}"


class Client(models.Model):
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)