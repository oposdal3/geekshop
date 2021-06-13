# Generated by Django 3.2.3 on 2021-06-13 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_productcategory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': ('продукт',), 'verbose_name_plural': 'продукты'},
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products_images', verbose_name='фото товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_desc',
            field=models.CharField(blank=True, max_length=60, verbose_name='карткое описание товара'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='description',
            field=models.TextField(blank=True, verbose_name='описание'),
        ),
    ]
