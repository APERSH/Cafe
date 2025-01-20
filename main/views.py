from django.http import HttpResponse
from django.shortcuts import render
from main.models import Table
from typing import Optional

def main(request) -> HttpResponse:
    """
    Представление для главной страницы. Для вывода списка столов (Table). 

    Аргументы:
    - request:

    Возвращает:
    - HttpResponse:
        Возвращает HTTP-ответ с отрендеренным шаблоном.
    """
    # Получаем параметр 'q' из GET-запроса
    query: Optional[str] = request.GET.get('q', None)

    # Если 'q' присутствует в запросе, фильтруем столы по ID.
    if query:
        tables = Table.objects.filter(id=int(query))
    else:
        tables = Table.objects.all()
    context = {
        'title' : 'Главная',
        'tables': tables,
    } 
    return render(request, 'main/main.html', context)
