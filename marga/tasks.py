from __future__ import absolute_import, unicode_literals
from rmscraper.celery import app
from celery.schedules import crontab

from marga.models import Url, Store
from marga.utils import *

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



# app.conf.beat_schedule = {
#     'periodic_addinfotodb': {
#         'task': 'marga.tasks.periodic_addinfotodb',
#         'schedule': 30.0,
#     },
# }

# @app.task
# def add(x, y):
#     z = x + y
#     print(z)
#     return

# app.conf.beat_schedule = {
#     'rl-scheduled-task': {
#         'task': 'marga.tasks.task_addinfotodb',
#         'schedule': 10.0,
#         'args': (1),
#     },
# }