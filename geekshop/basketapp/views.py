from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    basket = []
    count_products = 0
    total_price_product = 0

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    for el in basket:
        count_products += el.quantity
        total_price_product += el.product.price * el.quantity

    context = {
        'basket': basket,
        'count_products': count_products,
        'total_price_product': total_price_product,
    }

    return render(request, 'basketapp/basket.html', context=context)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request):
    pass

