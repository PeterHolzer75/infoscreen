from django.contrib import admin
from django.urls import path, include
# from boendelista import views
from . import views

app_name = 'resurser'

urlpatterns = [

    path('<str:adress>/', views.resurser, name='resurser'),
    
]
