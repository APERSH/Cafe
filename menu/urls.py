from django.urls import path
from menu import views

app_name = 'menu'

urlpatterns = [
    path('<int:table_id>/', views.catalog, name='catalog')
]
