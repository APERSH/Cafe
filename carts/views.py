from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from menu.models import Product
from carts.models import Cart
from main.models import Table

def cart_add(request, product_slug : str, table_id : int) -> HttpResponseRedirect:
    """
    Добавляет продукт (Product) в корзину (Cart) для конкретного стола (Table). 

    Аргументы:
    - request: 
    - product_slug: str
        Уникальный идентификатор продукта (slug).
    - table_id: int
        Уникальный идентификатор стола.

    Возвращает:
    - HttpResponseRedirect:
        Перенаправление на предыдущую страницу.
    """
    table = get_object_or_404(Table, id = table_id)
    product = get_object_or_404(Product, slug=product_slug)
    carts = Cart.objects.filter(table=table, product=product)
    if carts.exists():
        cart = carts.first()
        if cart:
            cart.quantity+=1
            cart.save()
    else:
        Cart.objects.create(table=table, product=product, quantity = 1)
    return redirect(request.META['HTTP_REFERER'])

def cart_add_quantity(request, cart_id : int) -> HttpResponseRedirect:
    """
    Добавляет количество продукта (Product) на 1 в корзине (Cart) для конкретного стола (Table). 

    Аргументы:
    - request: 
    - cart_id: int
        Уникальный идентификатор корзины.

    Возвращает:
    - HttpResponseRedirect:
        Перенаправление на предыдущую страницу.
    """
    carts = Cart.objects.get(id=cart_id)
    carts.quantity+=1
    carts.save()
    return redirect(request.META['HTTP_REFERER'])

def cart_subtract_quantity(request, cart_id: int) -> HttpResponseRedirect:
    """
    Убавляет количество продукта (Product) на 1 в корзине (Cart) для конкретного стола (Table).
    Если количество товара равно 1, то при убавлении количества он удаляется 

    Аргументы:
    - request: 
    - cart_id: int
        Уникальный идентификатор корзины.

    Возвращает:
    - HttpResponseRedirect:
        Перенаправление на предыдущую страницу.
    """
    carts = Cart.objects.get(id=cart_id)
    if carts.quantity==1:
        carts.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        carts.quantity-=1
        carts.save()
        return redirect(request.META['HTTP_REFERER'])

def cart_remove(request, cart_id : int) -> HttpResponseRedirect:
    """
    Удаляет продукт (Product) из корзины (Cart) для конкретного стола (Table).
    

    Аргументы:
    - request: 
    - cart_id: int
        Уникальный идентификатор корзины.

    Возвращает:
    - HttpResponseRedirect:
        Перенаправление на предыдущую страницу.
    """
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])
