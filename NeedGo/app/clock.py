import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from .mapbox_manager import update_mapbox

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', id='update_mapbox_function_id', minute='*')
def update_mapbox_function():

    """
    CRON job to update mapbox.
    TRIGGER: Every minute.
    """

    update_mapbox()


scheduler.start()
