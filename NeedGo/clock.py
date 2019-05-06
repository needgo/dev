import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NeedGo.settings")
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

from .app import mapbox_manager

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', id='update_mapbox_function_id', minute='*')
def update_mapbox_function():

    """
    CRON job to update mapbox.
    TRIGGER: Every minute.
    """

    mapbox_manager.update_mapbox()


scheduler.start()
