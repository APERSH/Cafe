from django.contrib import admin
from main.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_of_seats', 'is_free']
