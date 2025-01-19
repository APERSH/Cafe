from django.shortcuts import render
from main.models import Table

def main(request):

    query = request.GET.get('q', None)

    if query:
        tables = Table.objects.filter(id=int(query))
    else:
        tables = Table.objects.all()
    context = {
        'title' : 'Главная',
        'tables': tables,
    } 
    return render(request, 'main/main.html', context)
