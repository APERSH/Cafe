from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('cart_add/<slug:product_slug>/<int:table_id>/', views.cart_add, name='cart_add'),
    path('cart_add_quantity/<int:cart_id>/', views.cart_add_quantity, name='cart_add_quantity'),
    path('cart_subtract_quantity/<int:cart_id>/', views.cart_subtract_quantity, name='cart_subtract_quantity'),
    path('cart_remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
]