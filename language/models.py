from django.db import models

class Language(models.Model):
    uzb = models.TextField(verbose_name="O'zbekcha")
    rus = models.TextField(verbose_name="Ruscha")

    class Meta:
        verbose_name = "Til sozlamasi"
        verbose_name_plural = "Til sozlamalari"

    def __str__(self):
        return self.uzb


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