from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
import socket
import requests
import json
import pickle
import os
import math
from PIL import Image

# IP address


def resurser(request, adress):
    # adress = 'Grönkullagatan 9B'
    template_name = 'resurser/resurser.html'

    proxyDict = {
        "http": os.environ.get('FIXIE_URL', ''),
        "https": os.environ.get('FIXIE_URL', '')
    }

    url_r = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusresurslista?gatuadress=' + adress

    img_barray = 'https: // biztalk.helsingborgshem.se/Integration.Api/dataexport/testclient/testbild?file=testbild'
    print(img_barray)

    if settings.DEBUG == False:

        r = requests.get(url_r, proxies=proxyDict)
        if r.status_code != 200:
            return HttpResponse(f'<h3>Error {r.status_code}: Problem med API''et för resurslista</h3>')
        data_r = r.json()

    else:

        filename_r = 'resurslista29.data'
        with open(filename_r, 'rb') as filehandle:
            data_r = pickle.load(filehandle)

        img_barray = 'https: // biztalk.helsingborgshem.se/Integration.Api/dataexport/testclient/testbild?file=testbild'
        print(img_barray)

        bildfil = 'testbild.array'
        with open(bildfil, 'wb') as filehandle:
            pickle.dump(img_barray, filehandle)

    context = {
        'resurser': data_r,
    }

    return render(request, template_name, context)
