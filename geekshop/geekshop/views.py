from django.shortcuts import render
from django.shortcuts import render
from mainapp.views import get_products
from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    title = 'geekshop'
    products = get_products()[:4]
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'title': title,
        'products': products,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
    }
    return render(request, 'geekshop/contact.html', context=context)
