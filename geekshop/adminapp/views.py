from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from adminapp.forms import ShopUserRegisterForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import ShopUser
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from mainapp.models import Product, ProductCategory
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.contrib.auth.decorators import user_passes_test


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    ordering = '-is_active', '-is_staff', 'username'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icon'] = 'bx-user'
        context['title'] = 'Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    # fields = '__all__'  # get_form()

    def get_form(self, form_class=ShopUserRegisterForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, *args, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['icon'] = 'bx-user-plus'
        context['title'] = f'создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    context_object_name = 'edit_user'

    def get_form(self, form_class=ShopUserRegisterForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('adminapp:user_update', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f'пользователь: {context.get(self, self.object.username)}'
        context['title'] = title
        context['icon'] = 'bx-edit'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')
    context_object_name = 'user_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'удалить пользователя: {context.get(self, self.object.username)}'
        context['icon'] = 'bx-user_to_delete'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    ordering = '-is_active'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['icon'] = 'bx-cart'
        context['title'] = f'категории товаров'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_form(self, form_class=ProductCategoryEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, *args, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['icon'] = 'bx-category'
        context['title'] = f'Создание категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_form(self, form_class=ProductCategoryEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'категория: {context.get(self, self.object.name)}'
        context['icon'] = 'bx-edit'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')
    context_object_name = 'category_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'удалить категорию: {context.get(self, self.object.name)}'
        context['icon'] = 'bx-edit'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'
    ordering = '-is_active'
    paginate_by = 2

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk')).order_by('-is_active')

    def get_context_data(self, *args, object_lists=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context['icon'] = 'bx-cart'
        context['title'] = f'товары категории "{category.name}"'
        context['category'] = category
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin_staff:users')

    # initial = 'category': category
    # fields = '__all__'  # get_form()

    def get_initial(self):
        initial = super(ProductCreateView, self).get_initial()
        initial['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context['icon'] = 'bx-category'
        context['title'] = f'Добавить новый товар'
        context['category'] = category
        return context

    def get_form(self, form_class=ProductEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Детальная информация'
        context['icon'] = 'bx-chair'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'

    def get_form(self, form_class=ProductEditForm):
        """Вернет экземпляр формы, которая будет использоваться в этом представлении."""
        return form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Править: "{context.get(self, self.object.name)}"'
        context['icon'] = 'bx-edit'
        return context

    def get_success_url(self):
        return reverse_lazy('adminapp:product_read', args=(self.object.id,))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'удалить: {context.get(self, self.object.name)}'
        context['icon'] = 'bx-edit'
        return context

    def get_success_url(self):
        return reverse_lazy('adminapp:products', args=(self.object.category_id,))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}: ')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
