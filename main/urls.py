from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name = 'home'),
    path('search/', views.main, name = 'search')
]
