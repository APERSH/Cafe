from django.shortcuts import redirect, render, get_object_or_404
from menu.models import Product
from carts.models import Cart
from main.models import Table

def cart_add(request, product_slug, table_id):
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

def cart_add_quantity(request, cart_id):
    carts = Cart.objects.get(id=cart_id)
    carts.quantity+=1
    carts.save()
    return redirect(request.META['HTTP_REFERER'])

def cart_subtract_quantity(request, cart_id):
    carts = Cart.objects.get(id=cart_id)
    if carts.quantity==1:
        carts.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        carts.quantity-=1
        carts.save()
        return redirect(request.META['HTTP_REFERER'])

def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])
