from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import socket
import requests
import json
import pickle
import os
import math
import skanetrafiken as sk

proxyDict = {
    "http": os.environ.get('FIXIE_URL', ''),
    "https": os.environ.get('FIXIE_URL', '')
}

# IP address

def get_host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except:
        print("Unable to get Hostname and IP")
    return host_name, host_ip


def ip(request):
    return HttpResponse(f'<h1>IP-address: {get_host_name_IP()[1]} - Hostname: {get_host_name_IP()[0]}</h1>')


def infoscreen(request, adress):


    # adress = 'Grönkullagatan 9B'
    template_name = 'main/index.html'
    HAS_ACCESS = True

    proxyDict = {
        "http": os.environ.get('FIXIE_URL', ''),
        "https": os.environ.get('FIXIE_URL', '')
    }


    url_adressdata = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/objektadressinfo?gatuadress=' + adress
    url_b = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusboendelista_V2?gatuadress=' + adress
    url_r = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/trapphusresurslista?gatuadress=' + adress

    if HAS_ACCESS:

        adressdata = requests.get(url_adressdata, proxies=proxyDict)

        if adressdata.status_code != 200:
            return HttpResponse(f'<h3>Error {adressdata.status_code}: Problem med API för adressdata</h3>')

        b = requests.get(url_b, proxies=proxyDict)
        if b.status_code != 200:
            return HttpResponse(f'<h3>Error {b.status_code}: Problem med API för boendelista</h3>')
        data_b = b.json()

        r = requests.get(url_r, proxies=proxyDict)
        if r.status_code != 200:
            return HttpResponse(f'<h3>Error {r.status_code}: Problem med API för resurslista</h3>')
        data_r = r.json()

    else:

        filename_b = 'adresser29.data'
        filename_r = 'resurslista29.data'

        # with open(filename, 'wb') as filehandle:
        #     # store the data as binary data stream
        #     pickle.dump(j, filehandle)

        with open(filename_b, 'rb') as filehandle:
            data_b = pickle.load(filehandle)

        with open(filename_r, 'rb') as filehandle:
            data_r = pickle.load(filehandle)

    antal = len(data_b)
    print(f'len:{len(data_b)}')

    # OPenwheather API
    # api.openweathermap.org / data / 2.5 / weather ? q = London, uk & APPID = 9fc3e91e885cb4a9bd1efdd30313ecfb

    # tmeans = sk.trafficmeans()

    # ----------------------------------------------------------------------
    # Skånetrafiken API
    # ----------------------------------------------------------------------

    skr = sk.neareststation(56.0401881, 12.6988388, 0)

    # Code
    # Message
    # NearestStopAreas

    sa = skr["NearestStopAreas"]
    # Första träff är närmast
    nearest = sa[0]['Id']
    print(f'nearest: {nearest}')

    rp = sk.resultspage(f'Närmast|{nearest}|0',
                        "Helsingborg C|83241|0", "next")

    # rp = sk.resultspage("Malmö C|80000|0", "landskrona|82000|0", "next")
    # transportMode=("Stadsbuss",)

    jour = rp["Journeys"]  # class list

    # print(jour)
    # print(type(jour))

    # new_str = json.dumps(jour, indent=2, sort_keys=True)
    # new_str = json.dumps(jour, indent=2)
    # print('------------------------------------------------------------------------------------------------------')
    # print(new_str)
    # print('------------------------------------------------------------------------------------------------------')

    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    busstable = list()
    now = datetime.now()

    for sec in jour:
        # print(sec['SequenceNo'])
        rout = sec['RouteLinks']
        for r in rout:
            t = r['DepDateTime']
            tp = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
            diff = tp - now
            om_minuter = math.floor(diff.total_seconds() / 60)
            if om_minuter < 10:
                dep_time = f'{om_minuter} min'
            else:
                dep_time = t[11:16]

            busstable.append({'Name': r["Line"]['Name'],
                              'DepDateTime': dep_time,
                              'From': r['From']['Name'],
                              'Towards': r['Line']['Towards'],
                              'LineTypeName': r['Line']['LineTypeName']
                              })

    # print(busstable)

    # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    #     # print(rout['LineTypeName'])

    hn, ip = get_host_name_IP()

    context = {
        'data': data_b,
        'resurser': data_r,
        'busstable': busstable,
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
