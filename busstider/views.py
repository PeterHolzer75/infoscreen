import skanetrafiken as sk
from django.shortcuts import render

# Create your views here.


def buss(request):
    sk.querystation("Malmö C")
    sk.resultspage("Malmö C|80000|0", "landskrona|82000|0")
