from django.shortcuts import render, redirect
from django.db import transaction
from django.urls import reverse
from carts.models import Cart
from main.models import Table
from orders.models import Order, OrderItem


def create_order(request, table_id):
    table = Table.objects.get(id=table_id)
    carts = Cart.objects.filter(table=table)
    context = {
        'title':'Оформление заказа',
        'carts': carts,
        'table': table,
    }
    return render(request, 'orders/create_order.html', context)

def created_order(request, table_id):
    with transaction.atomic():
        table = Table.objects.get(id=table_id)
        cart_items = Cart.objects.filter(table=table)
        if cart_items.exists():
            order = Order.objects.create(
                table=table,
            )
            for cart_item in cart_items:
                product = cart_item.product
                name = cart_item.product.name
                price = cart_item.product.price
                quantity = cart_item.quantity

                OrderItem.objects.create(
                    order = order,
                    product = product,
                    name = name,
                    price = price,
                    quantity = quantity
                )
            cart_items.delete()
            table.is_free = 'busy'
            table.save()
            return render(request, 'orders/created_order.html')
        
def order_list(request):
    status_page = request.GET.get('status', None)
    query = request.GET.get('q', None)
    table_number = request.GET.get('table_number', None)
    if query:
        orders = Order.objects.filter(id=int(query))
    else:
        if table_number:
            orders = Order.objects.filter(table__id = table_number).order_by('id')
        else:
            orders = Order.objects.all().order_by('id')
        if status_page:
            orders = orders.filter(status = status_page).order_by('id')


    tables = Table.objects.all()
    
    context = {
        'orders': orders,
        'tables': tables
    }
    return render(request, 'orders/order_list.html', context) 

def order_remove(requset, order_id):
    order = Order.objects.get(id = order_id)
    order.delete()
    return redirect(requset.META['HTTP_REFERER'])




