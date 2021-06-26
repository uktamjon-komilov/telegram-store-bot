from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    description = models.TextField(verbose_name="Mahsulot haqida", blank=True)
    price = models.FloatField(verbose_name="Narxi", default=0.0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, verbose_name="Kategoriyasi")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    def __str__(self):
        return f"{self.product_name} - {self.category}"

