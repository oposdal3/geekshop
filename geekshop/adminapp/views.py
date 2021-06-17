from django.http import HttpResponseRedirect
from django.urls import reverse

from adminapp.forms import ShopUserRegisterForm, ProductEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.filter(is_delete=False).order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/рудактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserRegisterForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserRegisterForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_delete = True
        user.save()

        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


def category_create(request):
    pass


def category_update(request, pk):
    pass


def category_delete(request, pk):
    pass


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)

        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))

        context.update({'category': category})

        return context


def products(request, pk):
    title = 'админка/категории продуктов'

    if pk == 0:
        categories = ProductCategory.objects.filter(is_delete=False)

        context = {
            'title': title,
            'objects': categories,
        }

        return render(request, 'adminapp/categories.html', context=context)

    category = get_object_or_404(ProductCategory, pk=pk)
    products_category = Product.objects.filter(category__pk=pk)

    context = {
        'title': title,
        'category': category,
        'objects': products_category,
    }

    return render(request, 'adminapp/product_list.html', context=context)


def product_create(request, pk):
    title = 'продукты/создание'
    product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products'), args=[pk])
    else:
        product_form = ProductEditForm(initial={'category': product_category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': product_category
    }

    return render(request, 'adminapp/product_update.html', context)


def product_read(request, pk):

    product = get_object_or_404(ProductCategory, pk=pk)
    title = f'продукты/{product.name}'

    context = {
        'title': title,
        'product': product,
    }

    return render(request, 'adminapp/product_read.html', context)


def product_update(request, pk):
    product = get_object_or_404(ShopUser, pk=pk)
    title = f'продукты/рудактирование/{product.name}'

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[product_form.pk]))
    else:
        product_form = ProductEditForm(instance=product)

    context = {
        'title': title,
        'update_form': product_form,
        'category': product.category,
    }

    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = f'продукт/удаление/{product.name}'

    if request.method == 'POST':
        product.is_delete = True
        product.save()

        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
    }

    return render(request, 'adminapp/product_delete.html', context)
