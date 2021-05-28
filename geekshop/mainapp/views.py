from django.shortcuts import render


def products(request):
    title = 'каталог/продукты'

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    context = {
        'links_menu': links_menu,
        'title': title,
    }
    return render(request, 'products.html', context=context)
