from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Product, ProductCategory
from random import randint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.core.cache import cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
            print(cache)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    """
    Генерация случайного продукта
    :return: случайный продукт
    """
    products = get_products()
    # products = Product.objects.filter(is_active=True).all()
    # return random.sample(list(products), 1)[0]  # создан лишний объект list

    return products[randint(0, len(products) - 1)]


def get_same_product(hot_product):
    """
    Получение случайных продуктов из категории открытого горячего продукта
    :param hot_product: горячий продукт
    :return: список продуктов
    """
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    # same_products = Product.objects.filter(is_active=True).select_relatede('category').exclude(pk=hot_product.pk)[:3]

    return same_products


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['title'] = context.get(self, self.object.name)
        context['links_menu'] = get_links_menu()
        # context['links_menu'] = ProductCategory.objects.filter(is_active=True)
        return self.render_to_response(context)


def products(request, pk=None, page=1):
    title = 'Каталог товаров '
    links_menu = get_links_menu()
    # links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            # products = Product.objects.filter(is_active=True,category__is_active=True).order_by('price')
            products = get_products_orederd_by_price()
            title = f'Категория: "Все"'
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            # products = Product.objects.filter(category__pk=pk,is_active=True,category__is_active=True).order_by('price')
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)
            title = f'Категория: "{category.name}"'  # title, H2 Категория: "Дом"

        paginator = Paginator(products, 3)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator
        }

        return render(request, 'mainapp/products.html', context)

    # Главная страница каталога товаров
    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context)
