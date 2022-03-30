from urllib import response
from django.shortcuts import render
from django.http import HttpRequest
import requests
from bs4 import BeautifulSoup as bs

from marga.models import products
from rest_framework.viewsets import ModelViewSet

from marga.serializers import ProductsSerializer

def index(request):
    return render (request, "index.html")


def addurltodb(response):
    reply = ""
    if response.method == "POST":
        searched = (response.POST)["urluser"]
        if "https://barbora.lv/" not in searched and "https://www.rimi.lv/e-veikals/" not in searched:
            reply = "Saite ir nepareiza. Pievienot var tikai Rimi vai Barbora produkta vai produktu grupas saiti."
            print(reply)
        elif "https://www.rimi.lv/e-veikals/" in searched:
            u = (urls_rimi(url=searched))
            u.save()
            grab_rimi(str(searched))
            reply = "Rimi saite ir pievienota."
            print(reply)
        elif "https://barbora.lv/" in searched:
            u = (urls_barbora(url=searched))
            u.save()
            grab_barbora(str(searched))
            reply = "Barbora saite ir pievienota."
            print(reply)
        return render (response, "addurltodb.html")
    else:
        return render (response, "addurltodb.html")


def grab_rimi(baseurl):
    import requests
    from bs4 import BeautifulSoup as bs
    from datetime import datetime
        
    proxies = {"http": None, "https": None}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}

    baseurl = "https://www.rimi.lv/e-veikals/lv/produkti/piena-produkti-un-olas/jogurti-un-deserti/biezpiena-sierini/biezpiena-sierins-jeppi-ar-biskv-gars-kr-38g/p/946364"
    #baseurl = "https://www.rimi.lv/e-veikals/lv/produkti/piena-produkti-un-olas/siers/c/SH-11-9"
    #baseurl = "https://www.rimi.lv/e-veikals/lv/produkti/augli-un-darzeni/augli-un-ogas/banani/c/SH-2-1-3"

    pagecount = 1
    url = baseurl
    results = []

    r = requests.get(url, proxies=proxies, headers=headers)
    items = bs(r.text, 'html.parser').select('.side-cart-adapt')
    checkhowpages = bs(r.text, 'html.parser').select('.product-grid__item')
    
    if checkhowpages == []: #ja izveeleets tikai viens produkts
        items_title = items[1].select('.name')[0].text
        price_eur = items[1].select('div.price-wrapper')[0].select('.price span')[0].text
        price_cents = items[1].select('div.price-wrapper')[0].select('.price sup')[0].text
        items_price = float (price_eur + '.' + price_cents)
        items_oldprice = items[1].select('.price__old-price')
        if not items_oldprice:
            items_oldprice_value = None        
        else:
            items_oldprice_value = float (items_oldprice[0].text.replace("€", "").replace(",", "."))
        items_picture = items[1].select('.product__main-image')[0].select("img")[0].get("src")
        items_priceperunit = items[1].select('.price-per')[0].text.strip().replace("\n                ", "")
        results.append(dict(
            name = items_title,
            price = items_price,
            price_old = items_oldprice_value,
            price_per_unit = items_priceperunit,
            link_to_picture = items_picture,
            store_id = 1,
            #discount_period = items_discount_period,
        ))

    else: #ja izveeleeta produktu grupa

        pagination = bs(r.text, 'html.parser').select('.pagination__list .pagination__item')
        if pagination == []:
            pages = 1
        else:
            pages = int(pagination[len(pagination)-2].select("a")[0].get("data-page"))

        while pages >=1:

            print('\t URL:', url)  

            r = requests.get(url, proxies=proxies, headers=headers)

            items = bs(r.text, 'html.parser').select('.product-grid__item')

            for i in items:
                items_unavailable = i.select('.card__price-per')[0].text
                if not "Īslaicīgi nav pieejams" in items_unavailable:
                    items_title = i.select('.card__name')[0].text
                    price_eur = i.select('div.card__price-wrapper')[0].select('.price-tag span')[0].text
                    price_cents = i.select('div.card__price-wrapper')[0].select('.price-tag sup')[0].text
                    items_price = float (price_eur + '.' + price_cents)
                    items_oldprice = i.select('.old-price-tag')
                    if not items_oldprice:
                        items_oldprice_value = None
                    else:
                        items_oldprice_value = float (items_oldprice[0].text.replace("€", "").replace(",", "."))
                    items_picture = i.select('div.card__image-wrapper')[0].select("img")[0].get("src")
                    items_priceperunit = i.select('.card__price-per')[0].text.strip().replace("\n                    ", "")
                    results.append(dict(
                        name = items_title,
                        price = items_price,
                        price_old = items_oldprice_value,
                        price_per_unit = items_priceperunit,
                        link_to_picture = items_picture,
                        store_id = 1,
                        #discount_period = items_discount_period,
                    ))
            pages -= 1
            pagecount += 1
            url = baseurl + "?page=%i" % pagecount
            
    #rezultaatu pievienoshana db
    for res in results: 
        print(res)
        p = products(        
            name = res["name"],
            price = res["price"],
            price_old = res["price_old"],
            price_per_unit = res["price_per_unit"],
            link_to_picture = res["link_to_picture"],
            store_id = res["store_id"],
            #discount_period = res["discount_period"],
        )
        p.save()
    return render (request, "savetodb.html")


def grab_barbora(baseurl):

    proxies = {"http": None, "https": None}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}

    #baseurl = "https://barbora.lv/piena-produkti-un-olas/siers"
    baseurl = "https://barbora.lv/produkti/kukur-uzk-cheetos-ar-kecupa-garsu-165-g"

    pagecount = 1
    url = baseurl
    results = []
    
    while True:
        print('\t URL:', url)  
        r = requests.get(url, proxies=proxies, headers=headers)
        items = bs(r.text, 'html.parser').select('.b-product--desktop-grid')

        if items == []: #ja izveeleets tikai viens produkts
            items = bs(r.text, 'html.parser').select('.b-products-allow-desktop-view')
            items_title = items[0].select('.b-product-info--title')[0].text
            items_price = float (items[0].select('.b-product-price-current-number')[0].text.strip().replace("€", "").replace(",", "."))
            items_oldprice = items[0].select('.b-product-crossed-out-price')
            if not items_oldprice:
                items_oldprice_value = None
            else:
                items_oldprice_value = float (items_oldprice[0].text.replace("€", "").replace(",", "."))
            items_picture = items[0].select('.b-carousel--slide')[0].select("img")[0].get("src")
            items_priceperunit = items[0].select('.b-product-price--extra')[0].text.strip()
            results.append(dict(
                name = items_title,
                price = items_price,
                price_old = items_oldprice_value,
                price_per_unit = items_priceperunit,
                link_to_picture = items_picture,
                store_id = 2,
                #discount_period = items_discount_period,
            ))
            break

        #ja izveeleeta produktu grupa:
        pages = bs(r.text, 'html.parser').select('.b-pagination-wrapper .pagination li a')

        for i in items:
            items_unavailable = i.select('.b-product-unavailable--wrap')
            if not items_unavailable:
                items_title = i.select('.b-product-title--desktop')[0].text
                items_price = float (i.select('.b-product-price-current-number')[0].text.strip().replace("€", "").replace(",", "."))
                items_oldprice = i.select('.b-product-crossed-out-price')
                if not items_oldprice:
                    items_oldprice_value = None
                else:
                    items_oldprice_value = float (items_oldprice[0].text.replace("€", "").replace(",", "."))
                items_picture = i.select('.b-link--product-info')[0].select("img")[0].get("src")
                items_priceperunit = i.select('.b-product-price--extra')[0].text.strip()
                results.append(dict(
                    name = items_title,
                    price = items_price,
                    price_old = items_oldprice_value,
                    price_per_unit = items_priceperunit,
                    link_to_picture = items_picture,
                    #date_time_grab = datetime.now(),
                    store_id = 2,
                    #discount_period = items_discount_period,
                ))
        if str(pagecount) == pages[-2].text:
            break
        pagecount += 1
        url = baseurl + "?page=%i" % pagecount

    #rezultaatu pievienoshana db
    for res in results: 
        print(res)
        p = products(        
            name = res["name"],
            price = res["price"],
            price_old = res["price_old"],
            price_per_unit = res["price_per_unit"],
            link_to_picture = res["link_to_picture"],
            store_id = res["store_id"],
            #discount_period = res["discount_period"],
        )
        p.save()

    return render (request, "savetodb.html")
 
def searchdb (response):
    if response.method == "POST":
        searched = (response.POST)["itemname"]
        print (searched)
        reply = products.objects.filter(name__contains=searched).order_by("price")
        return render (response, "searchdb.html", {"reply": reply, "searched": searched})
    else:
        return render (response, "searchdb.html")

class productsview(ModelViewSet):
    queryset = products.objects.all()
    serializer_class = ProductsSerializer
