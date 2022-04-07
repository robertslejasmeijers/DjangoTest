from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpRequest

from marga.models import Product, Price, Url, Store
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from marga.serializers import ProductsSerializer

from marga.utils import *

def index(request):
    # u = (Store(name="RIMI"))
    # u.save()
    # u = (Store(name="BARBORA"))
    # u.save()
    # u = (Store(name="MAXIMA SIRSNĪGA"))
    # u.save()
    if request.user.is_authenticated == False:
        return redirect('login')
    return render(request, "marga/index.html")
    

def addurltodb(request):
    if request.user.is_authenticated == False:
        return redirect('login')
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
            u = (Url(url=searched, store_id=1, user_id=request.user.id))
            u.save()
            grab_rimi(str(searched))
            add_to_db(results, request)
            del results[:]
            reply = "Rimi saite ir pievienota."
            print(reply)
        elif "https://barbora.lv/" in searched:
            u = (Url(url=searched, store_id=2, user_id=request.user.id))
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


def addedurls(request):
    if request.user.is_authenticated == False:
        return redirect('login')
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


def addinfotodb(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    Product.objects.filter(user_id=request.user.id).delete()
    urlsfromdb = Url.objects.filter(user_id=request.user.id)
    for i in urlsfromdb: 
        print(i.url)
        if i.store_id == 1:
            grab_rimi(i.url)
        if i.store_id == 2:
            grab_barbora(i.url)
    #grab_maxima_sirsniga()
    global results
    add_to_db(results, request)
    del results[:]
    return render (request, "marga/addinfotodb.html")

#vecais bez nodaliitiem products un prices
# def searchdb (request):
#     if request.user.is_authenticated == False:
#         return redirect('login')
#     if request.method == "POST":
#         was_search=1
#         searched = (request.POST)["itemname"]
#         print (searched)
#         reply = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by("price")
#         return render (request, "marga/searchdb.html", {"reply": reply, "searched": searched, "was_search": was_search})
#     else:
#         return render (request, "marga/searchdb.html")

def searchdb (request):
    if request.user.is_authenticated == False:
        return redirect('login')
    if request.method == "POST":
        was_search=1
        searched = (request.POST)["itemname"]
        print (searched)
        reply = Product.objects.filter(user_id=request.user.id, name__icontains=searched)
        return render (request, "marga/searchdb.html", {"reply": reply, "searched": searched, "was_search": was_search})
    else:
        return render (request, "marga/searchdb.html")

class Productsview(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
