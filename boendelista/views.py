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

    proxyDict = {
        "http": os.environ.get('FIXIE_URL', ''),
        "https": os.environ.get('FIXIE_URL', '')
    }

    # adress = 'Grönkullagatan 9B'
    template_name = 'boendelista/boendelista.html'

    url_b = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusboendelista_V2?gatuadress=' + adress

    if settings.DEBUG == False:

        b = requests.get(url_b, proxies=proxyDict)
        if b.status_code != 200:
            return HttpResponse(f'<h3>Error {b.status_code}: Problem med API för boendelista</h3>')
        data_b = b.json()

    else:

        filename_b = 'adresser50.data'

        with open(filename_b, 'rb') as filehandle:
            data_b = pickle.load(filehandle)

    antal = len(data_b)

    print(f'Antal lägenheter: {antal}')

    context = {
        'data': data_b,
    }

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
        stl_vaning = 'font-size: .7rem;margin-bottom:0.4rem;'
        stl_namn_nummer = 'font-size: 0.6rem;'
        stl_rad = 'display: flex;justify-content: space-between;  padding-bottom: 0.3rem;'

    # HTML rendering
    # -----------------------------------------------------------------------
    # print(data_r)

    s = ''

    v_old = ''
    for adr in data_b:
        if adr['Vaning'] != v_old:
            if v_old != '':
                s += '</div>\n'
                s += '</div>\n'

            s += '<div class = "cont_vaning" >\n'
            s += f'<div class="vaning" style= "{stl_vaning};">\n'
            s += f'{adr["Vaningsbeteckning"]} </div>\n'

            s += '<div class= "rader">\n'

            v_old = adr['Vaning']

        s += f'<div class="rad" style = "{stl_rad}">\n'
        s += f'<div class="namn" style="{stl_namn_nummer}">{adr["Kund1Namn"]}'
        if adr['Kund2Namn']:
            s += f', {adr["Kund2Namn"]}'
        s += '</div>\n'
        s += f'<div class="nummer" style="{stl_namn_nummer}">' + \
            adr['Lagenhetsnummer'] + '</div>\n'

        s += '</div>\n'
    s += '</div>\n'
    s += '</div>\n'

    context['boendelista'] = s

    return render(request, template_name, context)
