from django.shortcuts import render
from orders.models import Order
from django.utils import timezone

def profit_list(request):
    today = timezone.now().date()
    orders = Order.objects.filter(status = 'paid', status_changed__date = today)
    profit = sum(order.total_cost() for order in orders)
    context = {
        'orders': orders,
        'profit' : profit
    }
    return render(request, 'profit/profit_list.html', context)
