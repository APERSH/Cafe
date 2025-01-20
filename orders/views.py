from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse
from carts.models import Cart
from main.models import Table
from orders.models import Order, OrderItem
from django.utils import timezone
from typing import Optional



def create_order(request, table_id : int) -> HttpResponse:
    """
    Представление для страницы оформления заказа. Функция извлекает объект стола по его ID 
    и отображает все товары в корзине для выбранного стола.

    Аргументы:
    - request: 
    - table_id: int
        Идентификатор стола, для которого оформляется заказ.

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с отрендеренным шаблоном.
    """
    # Получаем объект стола по его идентификатору
    table = Table.objects.get(id=table_id)
    # Получаем все товары в корзине для выбранного стола
    carts = Cart.objects.filter(table=table)
    context = {
        'title':'Оформление заказа',
        'carts': carts,
        'table': table,
    }
    return render(request, 'orders/create_order.html', context)

def created_order(request, table_id : int) ->HttpResponse:
    """
    Представление для создания заказа. Функция обрабатывает создание заказа для выбранного стола,
    используя элементы из корзины. После создания заказа корзина очищается, а стол становится занятым.

    Аргументы:
    - request: 
    - table_id: int
        Идентификатор стола, для которого создается заказ.

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с отрендеренным шаблоном.
    """
    # Использование транзакции для обеспечения атомарности операции
    with transaction.atomic():
        # Получаем объект стола по его идентификатору
        table = Table.objects.get(id=table_id)
        # Извлекаем все элементы корзины для выбранного стола
        cart_items = Cart.objects.filter(table=table)
        # Если в корзине есть товары, создаем заказ
        if cart_items.exists():
            # Создаем новый заказ для стола
            order = Order.objects.create(
                table=table,
            )
            # Переносим все товары из корзины в заказ
            for cart_item in cart_items:
                product = cart_item.product
                name = cart_item.product.name
                price = cart_item.product.price
                quantity = cart_item.quantity
                # Создаем элементы заказа для каждого товара из корзины
                OrderItem.objects.create(
                    order = order,
                    product = product,
                    name = name,
                    price = price,
                    quantity = quantity
                )
            # Удаляем все элементы из корзины после их переноса в заказ
            cart_items.delete()
            # Обновляем статус стола на "занят"
            table.is_free = 'busy'
            table.save()
            context = {
                'order': order,
                'title': 'Заказ успешно создан', 
            }
            return render(request, 'orders/created_order.html', context)
        
def order_list(request)->HttpResponse:
    """
    Представление для отображения списка заказов. Функция фильтрует заказы по различным параметрам, 
    включая статус, номер стола и ID заказа, если они присутствуют в GET-запросе.

    Аргументы:
    - request: 

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с отрендеренным шаблоном.
    """
    # Извлекаем параметры из GET-запроса
    status_page : Optional[str] = request.GET.get('status', None)
    query : Optional[str]= request.GET.get('q', None)
    table_number : Optional[str] = request.GET.get('table_number', None)
    # Фильтруем заказы в зависимости от переданных параметров
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
        'tables': tables,
        'title' : 'Список заказов'
    }
    return render(request, 'orders/order_list.html', context) 

def order_remove(requset, order_id : int) ->HttpResponseRedirect:
    """
    Представление для удаления заказа по его ID. Функция удаляет заказ из базы данных 
    и перенаправляет пользователя обратно на предыдущую страницу.

    Аргументы:
    - request: 
    - order_id: int
        Идентификатор заказа, который нужно удалить.

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с редиректом на предыдущую страницу.
    """
    # Получаем объект заказа по его ID
    order = Order.objects.get(id = order_id)
    # Удаляем заказ
    order.delete()
    return redirect(requset.META['HTTP_REFERER'])

def change_status(request) -> HttpResponseRedirect:
    """
    Представление для изменения статуса заказа. Функция обрабатывает POST-запрос, извлекает ID заказа
    и новый статус из данных формы, обновляет заказ и перенаправляет пользователя обратно на предыдущую страницу.

    Аргументы:
    - request:

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с редиректом на предыдущую страницу.
    """
    # Проверяем, что запрос имеет метод POST
    if request.method == 'POST':
        # Извлекаем ID заказа и новый статус из данных POST-запроса
        order_id = request.POST.get('order')
        status = request.POST.get('status')
        # Получаем заказ по его ID
        order = get_object_or_404(Order, id=order_id)
        # Обновляем статус заказа
        order.status = status
        # Фиксируем время изменения статуса
        order.status_changed = timezone.now()
        # Сохраняем изменения в базе данных
        order.save()
        return redirect(request.META['HTTP_REFERER'])



