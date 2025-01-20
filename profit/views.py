from django.http import HttpResponse
from django.shortcuts import render
from orders.models import Order
from django.utils import timezone

def profit_list(request) -> HttpResponse:
    """
    Представление для отображения списка оплаченных заказов за текущий день и расчета общей выручки.

    Аргументы:
    - request:

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с отрендеренным шаблоном.
    """
    # Текущая дата
    today = timezone.now().date()
    # Извлечение заказов со статусом 'paid' текущим днем
    orders = Order.objects.filter(status = 'paid', status_changed__date = today)
    # Расчет общей выручки
    profit = sum(order.total_cost() for order in orders)
    context = {
        'orders': orders,
        'profit' : profit,
        'title' : 'Выручка'
    }
    return render(request, 'profit/profit_list.html', context)
