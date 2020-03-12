from django.shortcuts import render
from django.http import HttpResponse
import socket
import requests
import json
import pickle
import os
import skanetrafiken as sk

# IP address


def get_host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except:
        print("Unable to get Hostname and IP")
    return host_name, host_ip


def boendelista(request, adress):
    # adress = 'Grönkullagatan 9B'

    HAS_ACCESS = False

    url_b = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/palyipptest/trapphusboendelista_V2?gatuadress=' + adress
    url_r = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/palyipptest/trapphusresurslista?gatuadress=' + adress

    if HAS_ACCESS:

        b = requests.get(url_b)
        data_b = b.json()

        r = requests.get(url_r)
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
    print(len(rp))

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

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    busstable = list()

    for sec in jour:
        # print(sec['SequenceNo'])
        rout = sec['RouteLinks']
        for r in rout:
            t = r['DepDateTime']
            t = t[11:16]
            print(t)
            # print(r["Line"]['Name'], r['DepDateTime'],
            #       r['Line']['Towards'], r['Line']['LineTypeName'])
            busstable.append({'Name': r["Line"]['Name'],
                              'DepDateTime': t,
                              'From': r['From']['Name'],
                              'Towards': r['Line']['Towards'],
                              'LineTypeName': r['Line']['LineTypeName']
                              })

    print(busstable)

    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

    #     # print(rout['LineTypeName'])

    template_name = 'main/index.html'
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
