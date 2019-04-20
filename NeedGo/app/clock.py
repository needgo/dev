import django

django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

from .mapbox_manager import update_mapbox

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', id='update_mapbox', minute='*')
def update_mapbox():

    """
    CRON job to update mapbox.
    TRIGGER: Every minute.
    """

    update_mapbox()


scheduler.start()
