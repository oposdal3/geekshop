from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket

from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Product, ProductCategory
from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['title'] = context.get(self, self.object.name)
        context['links_menu'] = ProductCategory.objects.filter(is_active=True)
        return self.render_to_response(context)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)


def products(request, pk=None):
    title = 'каталог/продукты'
    links_menu = ProductCategory.objects.all()

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')
        context = {
            'products': products,
            'title': title,
            'category': category,
            'links_menu': links_menu,
        }
        return render(request, 'products.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'products.html', context=context)


