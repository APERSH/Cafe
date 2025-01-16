from django.db import models
from main.models import Table
from menu.models import Product

class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)    

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE, verbose_name='Стол')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveBigIntegerField(default=0, verbose_name='Количество')
    create_timestamp = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины' 

    objects = CartQueryset().as_manager()

    def __str__(self) -> str:
        return f'Стол {self.table.pk} | Товар {self.product.name} | Количество {self.quantity}'
    
    def products_price(self):
        return round(self.product.price * self.quantity, 2)
