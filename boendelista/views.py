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

    template_name = 'boendelista/boendelista.html'

    url_b = f'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusboendelista_v2?gatuadress={adress}'

    # if 1 == 0:
    if settings.DEBUG == False:
        b = requests.get(url_b, proxies=proxyDict)
        if b.status_code not in range(200, 299):
            return HttpResponse(f'<h3>Error {b.status_code}: Problem med API för boendelista</h3>')
        data_b = b.json()
    else:
        # filename_b = 'boende_sallbo.data'
        filename_b = 'adresser6.data'
        with open(filename_b, 'rb') as filehandle:
            data_b = pickle.load(filehandle)

    antal = len(data_b)

    print(f'Antal lägenheter: {antal}')

    context = {
        # 'data': data_b,
    }

    context['antal'] = antal
    context['gatuadress'] = adress

    # Font-sizes

    # -----------------------------------------------------------------------
    stl_vaning = 'vaning-1'
    stl_rad = 'rad-1'
    stl_namn_nummer = 'namn_nummer-1'

    if antal >= 50:
        stl_vaning = 'vaning-50'
        stl_rad = 'rad-50'
        stl_namn_nummer = 'namn_nummer-50'

    # HTML rendering
    # -----------------------------------------------------------------------
    # print(data_b)

    print(stl_vaning)

    s = ''
    v_old = ''
    for adr in data_b:
        if adr['Vaning'] != v_old:
            if v_old != '':
                s += '</div>\n'
                s += '</div>\n'

            s += '<div class= "hr_imellan"></div>\n'
            s += '<div class = "cont_vaning" >\n'
            s += f'<div class="{stl_vaning}">'
            s += f'{adr["Vaning"]} </div>\n'
            s += '<div class= "rader">\n'

            v_old = adr['Vaning']
        s += f'<div class= "{stl_rad}">\n'
        s += f'<div class="{stl_namn_nummer}" >{adr["Kund1Namn"]}'
        if adr['Kund2Namn']:
            s += f', {adr["Kund2Namn"]}'
        s += '</div>\n'
        s += f'<div class="{stl_namn_nummer}">' + \
            adr['Lagenhetsnummer'] + '</div>\n'
        s += '</div>\n'

    s += '</div>\n'
    s += '</div>\n'
    # return HttpResponse(s)

    context['boendelista'] = s
    print(s)

    return render(request, template_name, context)
