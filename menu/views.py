from django.http import HttpResponse
from django.shortcuts import render
from main.models import Table
from menu.models import Product

def catalog(request, table_id : int) -> HttpResponse:
    """
    Представление для страницы меню. Извлекаем стол по его ID 
    и отображаем все доступные продукты в меню.

    Аргументы:
    - request: 
    - table_id: int
        Идентификатор стола, для которого отображается меню.

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с отрендеренным шаблоном.
    """
    # Получаем стол по его идентификатору
    table = Table.objects.get(id=table_id)

    # Извлекаем все продукты
    products = Product.objects.all()
    context = {
        'table':table,
        'products': products,
        'title' : 'Меню'
    }
    return render(request, 'menu/catalog.html', context)

