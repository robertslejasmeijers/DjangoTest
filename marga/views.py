from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpRequest

from marga.models import Product, Price, Url, Store
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet

from marga.serializers import ProductsSerializer

from marga.utils import *
from .forms import Searchdb, Addurl, Deleteurl


# def index(request):
    # u = (Store(name="RIMI"))
    # u.save()
    # u = (Store(name="BARBORA"))
    # u.save()
    # u = (Store(name="MAXIMA SIRSNĪGA"))
    # u.save()
    # if request.user.is_authenticated == False:
    #     return redirect('login')
    # return render(request, "marga/index.html")
    

@login_required
def addurltodb(request):
    reply = ""
    global results
    allurls = Url.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        #searched = (request.POST)["urluser"]
        form_addurl = Addurl(request.POST)
        if form_addurl.is_valid():
            searched = form_addurl.cleaned_data["name"]
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
        form_addurl = Addurl()
        return render (request, "marga/addurltodb.html", {"reply": reply, "allurls": allurls, "form_addurl": form_addurl})
    else:
        form_addurl = Addurl
        return render (request, "marga/addurltodb.html", {"allurls": allurls , "form_addurl": form_addurl})


@login_required
def deleteurl(request):
    allurls = Url.objects.filter(user_id=request.user.id)
    form_deleteurl = Deleteurl
    if request.method == "POST":
        #searched = (request.POST)["deleteurl"]
        form_deleteurl = Deleteurl(request.POST)
        if form_deleteurl.is_valid():
            searched = form_deleteurl.cleaned_data["name"]
            if searched == "0":
                allurls.delete()
                reply = "Visas saites ir dzēstas"
                form_deleteurl = Deleteurl()
                return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})
            if searched.isnumeric() == True:
                if not Url.objects.filter(user_id=request.user.id, id=searched).exists():
                    reply = "Saite ar šādu ID neeksistē!"
                    form_deleteurl = Deleteurl()
                    return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})   
                Url.objects.filter(user_id=request.user.id, id=searched).delete()
                reply = "Dzēsta saite ar ID: " + str(searched)
                form_deleteurl = Deleteurl()
                return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})
            else:
                reply = "Nepareizi iedvadīts ID"
                form_deleteurl = Deleteurl()
                return render (request, "marga/deleteurl.html", {"allurls": allurls, "reply": reply, "form_deleteurl": form_deleteurl})
    else:
        return render (request, "marga/deleteurl.html", {"allurls": allurls, "form_deleteurl": form_deleteurl})


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
    if len(Url.objects.filter(user_id=request.user.id)) and len(Product.objects.filter(user_id=request.user.id)) == 0:
        print("Nav saites")
        form = Searchdb
        return render (request, "marga/index.html", {"form": form})
    if request.method == "POST":
        #searched = request.POST["search"]
        form = Searchdb(request.POST)
        if form.is_valid():
            searched = form.cleaned_data["name"]
    else:
        form = Searchdb
        searched = ""
    reply = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by("prices__price")
    reply = list(dict.fromkeys(reply)) #remove duplicates
    return render (request, "marga/index.html", {"reply": reply, "form": form})
      
            


def test(request):
    form = Searchdb
    return render(request, "marga/test.html", {"form": form})


def searchdbvalues(request):
    if request.method == "POST":
        was_search=1
        searched = (request.POST)["itemname"]
        print (searched)
        reply = Product.objects.filter(user_id=request.user.id, name__icontains=searched).order_by("prices__price").values("name", "link_to_picture", "store_id", "prices__price", "prices__price_old", "prices__price_per_unit", "prices__discount_period", "prices__date_time_grab")
        return render (request, "marga/test.html", {"reply": reply, "searched": searched, "was_search": was_search})
    else:
        return render (request, "marga/test.html")


def dbsortbypython (request):
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

