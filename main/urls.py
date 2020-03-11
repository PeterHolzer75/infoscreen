from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    # path('boendelista/<str:adress>', views.boendelista, name='boendelista'),
    path('<str:adress>', views.boendelista, name='boendelista'),
]
