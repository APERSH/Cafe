from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/<int:table_id>/', views.create_order, name='create-order'),
]