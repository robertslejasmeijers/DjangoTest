from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpRequest

from marga.models import Product, Price, Url, Store
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet

from marga.serializers import ProductsSerializer

from marga.utils import *
from .forms import Searchdb


@login_required
def index(request):
    # u = (Store(name="RIMI"))
    # u.save()
    # u = (Store(name="BARBORA"))
    # u.save()
    # u = (Store(name="MAXIMA SIRSNĪGA"))
    # u.save()
    # if request.user.is_authenticated == False:
    #     return redirect('login')
    return render(request, "marga/index.html")
    

@login_required
def addurltodb(request):
    reply = ""
    global results
    if request.method == "POST":
        searched = (request.POST)["urluser"]
        if "https://barbora.lv/" not in searched and "https://www.rimi.lv/e-veikals/" not in searched:
            reply = "Saite ir nepareiza. Pievienot var tikai Rimi vai Barbora produkta vai produktu grupas saiti."
            print(reply)
        if Url.objects.filter(url=searched, user_id=request.user.id).exists():
            reply = "Kļūda! Šī saite jau bija pievienota!"
            print(reply)
        elif "https://www.rimi.lv/e-veikals/" in searched:
            u = (Url(url=searched, store_id=Store.RIMI_ID, user_id=request.user.id))
            u.save()
            grab_rimi(str(searched))
            add_to_db(results, request)
            del results[:]
            reply = "Rimi saite ir pievienota."
            print(reply)
        elif "https://barbora.lv/" in searched:
            u = (Url(url=searched, store_id=Store.BARBORA_ID, user_id=request.user.id))
            u.save()
            grab_barbora(str(searched))
            add_to_db(results, request)
            del results[:]
            reply = "Barbora saite ir pievienota."
            print(reply)
        allurls = Url.objects.filter(user_id=request.user.id)
        return render (request, "marga/addurltodb.html", {"reply": reply, "searched": searched, "allurls": allurls})
    else:
        return render (request, "marga/addurltodb.html")


@login_required
def addedurls(request):
    allurls = Url.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        searched = (request.POST)["deleteurl"]
        if searched == "visas":
            allurls.delete()
            reply = "Visas saites ir dzēstas"
            return render (request, "marga/addedurls.html", {"allurls": allurls, "reply": reply})
        if searched.isnumeric() == True:
            Url.objects.filter(user_id=request.user.id, id=searched).delete()
            reply = "Dzēsta saite ar ID: " + str(searched)
            return render (request, "marga/addedurls.html", {"allurls": allurls, "reply": reply})
        else:
            reply = "Nepareizi iedvadīts ID"
            return render (request, "marga/addedurls.html", {"allurls": allurls, "reply": reply})
    else:
        return render (request, "marga/addedurls.html", {"allurls": allurls})


@login_required
def addinfotodb(request):
    #Product.objects.filter(user_id=request.user.id).delete()
    urlsfromdb = Url.objects.filter(user_id=request.user.id)
    for i in urlsfromdb: 
        print(i.url)
        if i.store_id == Store.RIMI_ID:
            grab_rimi(i.url)
        if i.store_id == Store.BARBORA_ID:
            grab_barbora(i.url)
    #grab_maxima_sirsniga()
    global results
    add_to_db(results, request)
    del results[:]
    return render (request, "marga/addinfotodb.html")


@login_required
def searchdb (request):
    form = Searchdb
    if request.method == "POST":
        was_search=1
        searched = (request.POST)["itemname"]
        print (searched)
        reply = Product.objects.filter(user_id=request.user.id, name__icontains=searched)
        return render (request, "marga/searchdb.html", {"reply": reply, "searched": searched, "was_search": was_search, "form": form})
    else:
        return render (request, "marga/searchdb.html")


def test (request):
    sort_by = request.GET.get('sort_by', None)
    prices = Price.objects.all()
    prices_and_products = []
    for i in prices:
        item = {"name": i.product.name, "store": i.product.store.name, "price": i.price, "date": i.date_time_grab}
        prices_and_products.append(item)
    if sort_by:
        def sort_key(item):
            return (item[sort_by], item['date'])
        #prices_and_products.sort(key=sort_key)
        prices_and_products.sort(key=lambda k: (k[sort_by], k["date"]))
        print (prices_and_products)
    return render (request, "marga/test.html", {"prices_and_products": prices_and_products})


class Productsview(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


