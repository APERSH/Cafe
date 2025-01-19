from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('search/', views.order_list, name='search'),
    path('create-order/<int:table_id>/', views.create_order, name='create-order'),
    path('created-order/<int:table_id>/', views.created_order, name='created-order')
]