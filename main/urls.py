from django.contrib import admin
from django.urls import path, include
from main import views

app_name = 'main'
urlpatterns = [
    path('ip/', views.ip),
    path('<str:adress>', views.infoscreen, name='infoscreen'),

]
