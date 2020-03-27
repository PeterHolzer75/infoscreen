
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


# IP address

def kollektivtrafik(request, adress):
    # adress = 'Grönkullagatan 9B'

    print

    template_name = 'kollektivtrafik/kollektivtrafik.html'
    
    url_adressdata = 'https://biztalk.helsingborgshem.se/integration.api/dataexport/playipptest/objektadressinfo?gatuadress=' + adress

    # ----------------------------------------------------------------------
    # Skånetrafiken API
    # ----------------------------------------------------------------------
    
    adressdata = requests.get(url_adressdata)

    print(adressdata.headers)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(adressdata.status_code)
    print(adressdata)
    a = adressdata.json()
    print(a)
    lat = a[0]['Lat']
    lng = a[0]['Lng']
       
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    

    if adressdata.status_code !=200:            
        return HttpResponse(f'<h3>Error {adressdata.status_code}: Problem med API för adressdata</h3>')

    skr = sk.neareststation(lat,lng, 0)

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

    print(jour)
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



    context = {
        'busstable': busstable,
    }
    return render(request, template_name, context)