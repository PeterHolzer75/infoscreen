from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
import socket
import requests
import json
import pickle
import os


def boendelista(request, adress):

    # --  FIXIE_URL = http://fixie:Uud9w5EzrZweESt@olympic.usefixie.com:80

    # proxyDict = {
    #     "http": os.environ.get('FIXIE_URL', ''),
    #     "https": os.environ.get('FIXIE_URL', '')
    # }

    template_name = 'boendelista/boendelista.html'

    url_b = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusboendelista_V2?gatuadress=' + adress

    if False:
        # if settings.DEBUG == False:

        b = requests.get(url_b, proxies=proxyDict)

        if b.status_code != 200:
            return HttpResponse(f'<h3>Error {b.status_code}: Problem med API för boendelista</h3>')
        data_b = b.json()

    else:

        filename_b = 'boende_sallbo.data'
        with open(filename_b, 'rb') as filehandle:
            data_b = pickle.load(filehandle)

    antal = len(data_b)

    print(f'Antal lägenheter: {antal}')

    context = {
        'allaboende': data_b,
    }

    print(data_b)

    context['antal'] = antal
    context['gatuadress'] = adress

    # Font-sizes
    # -----------------------------------------------------------------------
    stl_vaning = 'font-size: 0.8rem;margin-bottom:0.5rem;'
    stl_namn_nummer = 'font-size: 0.7rem;'
    stl_rad = 'display: flex;justify-content: space-between;  padding-bottom: 0.4rem;'

    if antal >= 30:
        stl_vaning = 'font-size: 1.0rem;margin-bottom:0.5rem;'
        stl_namn_nummer = 'font-size: 0.7rem;'
        stl_rad = 'display: flex;justify-content: space-between;  padding-bottom: 0.4rem;'

    if antal >= 50:
        stl_vaning = 'font-size: .7rem; margin-bottom:0.4rem;'
        stl_namn_nummer = 'font-size: 0.5rem;'
        stl_rad = 'display: flex;justify-content: space-between;  padding-bottom: 0.21rem;'

        # HTML rendering
        # -----------------------------------------------------------------------
        # print(data_r)

    return render(request, template_name, context)
