from django.urls import path
import basketapp.views as basket

urlpatterns = [
    path('', basket.basket, name='basket'),
    path('add/<int:pk>/', basket.basket_add, name='add'),
    path('remove/<int:pk>/', basket.basket_remove, name='remove'),
]
