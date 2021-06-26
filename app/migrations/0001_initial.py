# Generated by Django 3.2.4 on 2021-06-26 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, verbose_name='Kategoriya nomi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Mahsulot nomi')),
                ('description', models.TextField(blank=True, verbose_name='Mahsulot haqida')),
                ('price', models.FloatField(default=0.0, verbose_name='Narxi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.category', verbose_name='Kategoriyasi')),
            ],
        ),
    ]
