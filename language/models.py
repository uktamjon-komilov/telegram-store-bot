from django.db import models

class Language(models.Model):
    uzb = models.TextField(verbose_name="O'zbekcha")
    rus = models.TextField(verbose_name="Ruscha")

    class Meta:
        verbose_name = "Til sozlamasi"
        verbose_name_plural = "Til sozlamalari"

    def __str__(self):
        return self.uzb