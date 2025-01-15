from django.shortcuts import render
from main.models import Table

def main(request):
    tables = Table.objects.all()
    context = {
        'title' : 'Главная',
        'tables': tables,
    }
    return render(request, 'main/main.html', context)
