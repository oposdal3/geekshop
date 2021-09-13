from functools import cached_property

from django.db import models

from django.conf import settings

from basketapp.models import Basket
from mainapp.models import Product


class OrderItemQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(
        verbose_name='статус',
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING
    )
    is_active = models.BooleanField(db_index=True, verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)  # сортировка по умолчанию от более новых к старым заказам
        verbose_name = 'заказ'  # имя класса в единственном числе
        verbose_name_plural = 'заказы'  # имя класса во множественном числе

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    @cached_property
    def get_items_cached(self):
        return self.orderitems.select_related()

    def get_total_quantity(self):
        """
        select_related работает путем создания соединения SQL и включения полей связанного объекта в оператор SELECT.
        По этой причине select_related получает связанные объекты в том же запросе к базе данных.
        :return:
        """
        items = self.get_items_cached  # выбираем все дочерние элементы заказа
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.get_items_cached
        return len(items)

    def get_total_cost(self):
        items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.get_items_cached:
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.get_items_cached
        return {
            'get_total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'get_total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def get_name_order(self):
        print('Заказ', type(self.updated))
        return f'Заказ № {self.pk} от {self.created.strftime("%d.%m.%Y")}'


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(
        Order,
        related_name="orderitems",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    def get_product_cost(self):
        return self.product.price * self.quantity

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()

        super(self.__class__, self).delete()
