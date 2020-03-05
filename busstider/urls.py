from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'skanetrafiken'

urlpatterns = [
    # path('boendelista/<str:adress>', views.boendelista, name='boendelista'),
    path('', views.buss, name='buss'),
]
