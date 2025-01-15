from django.shortcuts import render
from main.models import Table
from menu.models import Product

def catalog(request, table_id):
    table = Table.objects.get(id=table_id)
    products = Product.objects.all()
    context = {
        'table':table,
        'products': products
    }
    return render(request, 'menu/catalog.html', context)

