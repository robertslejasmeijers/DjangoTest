from __future__ import absolute_import, unicode_literals
from rmscraper.celery import app
from celery.schedules import crontab

from marga.models import Url, Store
from marga.utils import *

import logging
logger = logging.getLogger(__name__)

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=13, hour=3), periodic_addinfotodb.s(), name='periodic_addinfotodb')


@app.task
def ondemand_addinfotodb(userid):
    urlsfromdb = Url.objects.filter(user_id=userid)
    for i in urlsfromdb: 
        if i.store_id == Store.RIMI_ID:
            grabresults = grab_rimi(i.url, i.id)
            add_to_db(grabresults, userid)
        if i.store_id == Store.BARBORA_ID:
            grabresults = grab_barbora(i.url, i.id)
            add_to_db(grabresults, userid)
    grabresults = grab_maxima_sirsniga()
    add_to_db(grabresults, userid)
    logger.warning('ondemand_addinfotodb')
    return


@app.task
def periodic_addinfotodb():
    allusers = User.objects.all()
    for u in allusers:
        urlsfromdb = Url.objects.filter(user_id=u.id)
        for i in urlsfromdb: 
            if i.store_id == Store.RIMI_ID:
                grabresults = grab_rimi(i.url, i.id)
                add_to_db(grabresults, u.id)
            if i.store_id == Store.BARBORA_ID:
                grabresults = grab_barbora(i.url, i.id)
                add_to_db(grabresults, u.id)
        grabresults = grab_maxima_sirsniga()
        add_to_db(grabresults, u.id)
    return


@app.task
def ondemand_addurltodb(searched, userid):
    if "https://www.rimi.lv/e-veikals/" in searched:
        u = (Url(url=searched, store_id=Store.RIMI_ID, user_id=userid))
        u.save()
        url_id = Url.objects.filter(url=searched, user_id=userid)[0].id
        grabresults = grab_rimi(str(searched), url_id)
        if grabresults == []:
            logger.warning("Kļūda! No ievadītās RIMI saites neizdevās iegūt datus: " + searched)
            u.delete()
        else:
            addtodb_results = add_to_db(grabresults, userid)
            if addtodb_results == 1:
                logger.info("Produkts jau bija pievienots, un tā cena ir vienāda ar iepriekšējo cenu.")
                u.delete()
            if addtodb_results == 2:
                logger.info("Produkts jau bija pievienots, bet tā cena tika atjaunota.")
                u.delete()
            if addtodb_results == 0:
                logger.info("Rimi saite un tās produkti ir pievienoti.")
    if "https://barbora.lv/" in searched:
        u = (Url(url=searched, store_id=Store.BARBORA_ID, user_id=userid))
        u.save()
        url_id = Url.objects.filter(url=searched, user_id=userid)[0].id
        grabresults = grab_barbora(str(searched), url_id)
        if grabresults == []:
            logger.warning("Kļūda! No ievadītās BARBORA saites neizdevās iegūt datus: " + searched)
            u.delete()
        else:
            addtodb_results = add_to_db(grabresults, userid)
            if addtodb_results == 1:
                logger.info("Produkts jau bija pievienots, un tā cena ir vienāda ar iepriekšējo cenu.")
                u.delete()
            if addtodb_results == 2:
                logger.info("Produkts jau bija pievienots, bet tā cena tika atjaunota.")
                u.delete()
            if addtodb_results == 0:
                logger.info("Barbora saite un tās produkti ir pievienoti.")
    return



# app.conf.beat_schedule = {
#     'periodic_addinfotodb': {
#         'task': 'marga.tasks.periodic_addinfotodb',
#         'schedule': 30.0,
#     },
# }

