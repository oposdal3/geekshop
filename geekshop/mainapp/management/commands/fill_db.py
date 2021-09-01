import json
import os
from geekshop.config import SUPER_USER_LOGIN, SUPER_USER_EMAIL, SUPER_USER_PASSWORD

from authapp.models import ShopUser
from django.core.management.base import BaseCommand

from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    # with open(os.path.join(JSON_PATH, file_name + '.json'), mode = 'r', encoding= 'utf-8') as infile:
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)  # распаковка всех полей
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_pk = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(pk=category_pk)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # Создаем суперпользователя при помощи менеджера модели
        ShopUser.objects.create_superuser(SUPER_USER_LOGIN, SUPER_USER_EMAIL, SUPER_USER_PASSWORD, age='22', )

# manage.py dumpdata > db.json  # Все таблицы
# manage.py dumpdata mainapp.productcategory > mainapp/json/categories.json
# manage.py dumpdata mainapp.product > mainapp/json/products.json  # product
# manage.py fill_db.py
