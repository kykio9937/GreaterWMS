from django.urls import path
from . import views

urlpatterns = [
path('', views.login, name='login'),
path('send_code/', views.send_code, name='send_code')
]
