import os
import django
from requests import post
from requests.exceptions import RequestException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeedGo.settings')
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', id='update_mapbox_function_id', minute='*')
def update_mapbox_function():

    """
    CRON job to update mapbox.
    TRIGGER: Every minute.
    """

    # Mapbox configuration
    token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

    url = "https://api.mapbox.com/uploads/v1/needgo?access_token="+token
    params = {
        "tileset": "needgo.cjuojgd9c01z632la84qa1v61-0fykf",
        "url": "mapbox://datasets/needgo/cjuojgd9c01z632la84qa1v61",
        "name": "cjuojgd9c01z632la84qa1v61-0fykf"
    }

    try:
        request = post(url, json=params)
        response = request.text
    except RequestException:
        print("EXCEPTION")
        response = "Error saving record in mapbox"

    return response


scheduler.start()