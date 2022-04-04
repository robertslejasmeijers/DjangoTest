from urllib import response
from django.shortcuts import render
from django.http import HttpRequest

from marga.models import Product, Url, Store
from rest_framework.viewsets import ModelViewSet

from marga.serializers import ProductsSerializer

import requests
from bs4 import BeautifulSoup as bs
import json

from marga.utils import *

def index(request):
    return render (request, "marga/index.html")


def addurltodb(response):
    reply = ""
    global results
    if response.method == "POST":
        searched = (response.POST)["urluser"]
        if "https://barbora.lv/" not in searched and "https://www.rimi.lv/e-veikals/" not in searched:
            reply = "Saite ir nepareiza. Pievienot var tikai Rimi vai Barbora produkta vai produktu grupas saiti."
            print(reply)
        elif "https://www.rimi.lv/e-veikals/" in searched:
            u = (Url(url=searched, store_id=1))
            u.save()
            grab_rimi(str(searched))
            add_to_db(results)
            del results[:]
            reply = "Rimi saite ir pievienota."
            print(reply)
        elif "https://barbora.lv/" in searched:
            u = (Url(url=searched, store_id=2))
            u.save()
            grab_barbora(str(searched))
            add_to_db(results)
            del results[:]
            reply = "Barbora saite ir pievienota."
            print(reply)
        allurls = Url.objects.all()
        return render (response, "marga/addurltodb.html", {"reply": reply, "searched": searched, "allurls": allurls})
    else:
        return render (response, "marga/addurltodb.html")


def addedurls(response):
    allurls = Url.objects.all()
    if response.method == "POST":
        searched = (response.POST)["deleteurl"]
        if searched == "visas":
            Url.objects.all().delete()
            reply = "Visas saites ir dzēstas"
            return render (response, "marga/addedurls.html", {"allurls": allurls, "reply": reply})
        if searched.isnumeric() == True:
            Url(id=searched).delete()
            reply = "Dzēsta saite ar ID: " + str(searched)
            return render (response, "marga/addedurls.html", {"allurls": allurls, "reply": reply})
        else:
            reply = "Nepareizi iedvadīts ID"
            return render (response, "marga/addedurls.html", {"allurls": allurls, "reply": reply})
    else:
        return render (response, "marga/addedurls.html", {"allurls": allurls})


def addinfotodb(request):
    Product.objects.all().delete()
    urlsfromdb = Url.objects.all()
    for i in urlsfromdb: 
        print(i.url)
        if i.store_id == 1:
            grab_rimi(i.url)
        if i.store_id == 2:
            grab_barbora(i.url)
    grab_maxima_sirsniga()
    global results
    add_to_db(results)
    del results[:]
    return render (request, "marga/addinfotodb.html")


def searchdb (response):
    if response.method == "POST":
        was_search=1
        searched = (response.POST)["itemname"]
        print (searched)
        reply = Product.objects.filter(name__contains=searched).order_by("price")
        return render (response, "marga/searchdb.html", {"reply": reply, "searched": searched, "was_search": was_search})
    else:
        return render (response, "marga/searchdb.html")

class Productsview(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
