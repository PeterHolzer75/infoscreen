from django.contrib import admin
from django.urls import path, include
# from boendelista import views
from . import views

app_name = 'kollektivtrafik'

urlpatterns = [

    path('<str:adress>/', views.kollektivtrafik, name='kollektivtrafik'),
    
]
