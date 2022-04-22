from __future__ import absolute_import, unicode_literals
from rmscraper.celery import app


from marga.models import Url, Store
from marga.utils import *


# def add(x, y):
#     a= x + y
#     print (a)
#     return a

@app.task
def task_addinfotodb(userid):
    urlsfromdb = Url.objects.filter(user_id=userid)
    for i in urlsfromdb: 
        print(i.url)
        if i.store_id == Store.RIMI_ID:
            grabresults = grab_rimi(i.url, i.id)
            add_to_db(grabresults, userid)
        if i.store_id == Store.BARBORA_ID:
            grabresults = grab_barbora(i.url, i.id)
            add_to_db(grabresults, userid)
    grabresults = grab_maxima_sirsniga()
    add_to_db(grabresults, userid)
    return


# @app.task
# def task_addinfotodb(request):
#     urlsfromdb = Url.objects.filter(user_id=request.user.id)
#     for i in urlsfromdb: 
#         print(i.url)
#         if i.store_id == Store.RIMI_ID:
#             grabresults = grab_rimi(i.url, i.id)
#             add_to_db(grabresults, request)
#         if i.store_id == Store.BARBORA_ID:
#             grabresults = grab_barbora(i.url, i.id)
#             add_to_db(grabresults, request)
#     grabresults = grab_maxima_sirsniga()
#     add_to_db(grabresults, request)
#     return