from django.urls import path
from profit import views

app_name = 'profit'

urlpatterns = [
    path('',views.profit_list, name='profit-list' )
]
