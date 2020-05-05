
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from django.conf import settings
import socket
import requests
import json
import pickle
import os
import math
import skanetrafiken as sk


def kollektivtrafik(request, lat, lng):

    template_name = 'kollektivtrafik/kollektivtrafik.html'
    skr = sk.neareststation(lat, lng, 0)

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

    # print(type(jour))

    # new_str = json.dumps(jour, indent=2, sort_keys=True)
    # new_str = json.dumps(jour, indent=2)
    # print('------------------------------------------------------------------------------------------------------')
    # print(new_str)
    # print('------------------------------------------------------------------------------------------------------')

    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    busstable = list()
    now = datetime.now()

    timenow = datetime.now(tz=pytz.timezone('Europe/Copenhagen'))
    tn = timenow.replace(tzinfo=None)

    for sec in jour:
        rout = sec['RouteLinks']

        for r in rout:
            t = r['DepDateTime']

            print(f't:{t}')

            tp = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
            diff = tp - tn

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
        'busstable': busstable
    }
    context['autorefreshrate'] = 20

    return render(request, template_name, context)
