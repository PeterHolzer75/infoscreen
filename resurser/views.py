from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import socket
import requests
import json
import pickle
import os
import math

# IP address

def resurser(request, adress):
    # adress = 'Grönkullagatan 9B'
    template_name = 'main/index.html'

    HAS_ACCESS = True

    url_r = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusresurslista?gatuadress=' + adress

    if HAS_ACCESS:

        r = requests.get(url_r)
        if r.status_code !=200:            
            return HttpResponse(f'<h3>Error {r.status_code}: Problem med API för resurslista</h3>')
        data_r = r.json()

    else:

        filename_r = 'resurslista29.data'
        with open(filename_r, 'rb') as filehandle:
            data_r = pickle.load(filehandle)

    context = {
        'resurser': data_r,
    }


    return render(request, template_name, context)
