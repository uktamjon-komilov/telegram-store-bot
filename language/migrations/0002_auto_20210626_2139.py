# Generated by Django 3.2.4 on 2021-06-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'Til sozlamasi', 'verbose_name_plural': 'Til sozlamalari'},
        ),
        migrations.AlterField(
            model_name='language',
            name='rus',
            field=models.TextField(verbose_name='Ruscha'),
        ),
        migrations.AlterField(
            model_name='language',
            name='uzb',
            field=models.TextField(verbose_name="O'zbekcha"),
        ),
    ]