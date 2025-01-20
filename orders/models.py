from django.db import models
from main.models import Table
from menu.models import Product



class OrderitemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    STATUS_CHOICES = [
        ('wait', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table = models.ForeignKey(to=Table, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, verbose_name='Номер стола')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    status = models.CharField(verbose_name='Статус заказа', max_length=10, choices=STATUS_CHOICES, default='wait')
    status_changed = models.DateTimeField(null=True, blank=True, verbose_name='Дата изменения статуса')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы' 

    def __str__(self) -> str:
        return f'Заказ № {self.pk} | Стол {self.table.pk}'
    
    def total_cost(self):
        return sum(item.products_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, default=None, verbose_name='Продукт', related_name='order_items' )
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'


    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.price * self.quantity, 2)
    
    def __str__(self):
        return f' Товар {self.name} | Заказ № {self.order.pk}'