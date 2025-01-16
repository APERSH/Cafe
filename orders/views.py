from django.shortcuts import render
from django.db import transaction
from carts.models import Cart
from main.models import Table

def create_order(request, table_id):
    table = Table.objects.get(id=table_id)
    carts = Cart.objects.filter(table=table)
    context = {
        'title':'Оформление заказа',
        'carts': carts,
    }
    return render(request, 'orders/create_order.html', context)
