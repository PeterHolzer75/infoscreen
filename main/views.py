from django.shortcuts import render
from django.http import HttpResponse
import socket
import requests
import json
import pickle
import os

# IP address


def get_host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except:
        print("Unable to get Hostname and IP")
    return host_name, host_ip


def boendelista(request,adress):
    # adress = 'Grönkullagatan 9B'

    url_b = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/palyipptest/trapphusboendelista_V2?gatuadress=' + adress
    url_r = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/palyipptest/trapphusresurslista?gatuadress=' + adress
    

    b = requests.get(url_b)
    data_b = b.json()

    r = requests.get(url_r)
    data_r = r.json()


    filename_b = 'adresser29.data'
    filename_r = 'resurslista29.data'

    # with open(filename, 'wb') as filehandle:
    #     # store the data as binary data stream
    #     pickle.dump(j, filehandle)

    # with open(filename_b, 'rb') as filehandle:
    #     data_b = pickle.load(filehandle)

    # with open(filename_r, 'rb') as filehandle:
    #     data_r = pickle.load(filehandle)

    antal = len(data_b)
    print(f'len:{len(data_b)}')

    template_name = 'main/index.html'
    hn, ip = get_host_name_IP()

    context = {
        'data': data_b,
    'resurser': data_r
    }
    context['hn'] = hn
    context['ip'] = ip
    context['antal'] = antal
    context['gatuadress'] = adress
    

    # Font-sizes
    # -----------------------------------------------------------------------

    stl_vaning = 'font-size: 1rem;padding-top:0.3rem;margin-bottom:0.5rem;'
    stl_namn = 'font-size: 0.7rem;'
    stl_nummer = 'font-size: 0.7rem;'

    if antal >= 30:
        stl_namn = 'font-size: 0.8rem;'
        stl_nummer = 'font-size: 0.8rem;'
        stl_vaning = 'font-size: 1.2rem;'

    # stl_namn = 'font-size: 1.0rem;'
    # stl_nummer = 'font-size: 1.0rem;'
    # stl_vaning = 'font-size: 1.5rem;'

    # if antal >= 30:
    #     stl_namn = 'font-size: 0.8rem;'
    #     stl_nummer = 'font-size: 0.8rem;'
    #     stl_vaning = 'font-size: 1.2rem;'

    # HTML rendering
    # -----------------------------------------------------------------------
    # print(data_r)

    s = '<div class="lista">'

    v_old = ''
    for adr in data_b:
        if adr['Vaning'] != v_old:
            s += f'<div class="vaning" style= "{stl_vaning};">'
            s += adr['Vaning']
            s += '</div>'
            v_old = adr['Vaning']

        s += '<div class="rad">'
        s += f'<div class="namn" style="{stl_namn}">{adr["Kund1Namn"]}'
        if adr['Kund2Namn']:
            s += f', {adr["Kund2Namn"]}'
        s += '</div>'
        s += f'<div class="nummer" style="{stl_nummer}">' + \
            adr['Lagenhetsnummer'] + '</div >'

        s += '</div>'
    s += '</div>'

    # print(s)

    context['boendelista'] = s

    return render(request, template_name, context)
