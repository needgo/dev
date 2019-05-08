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

    print("ENTRA -------------------------------------------------")

    """
    CRON job to update mapbox.
    TRIGGER: Every minute.
    """

    # Mapbox configuration
    token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

    url = "https://api.mapbox.com/uploads/v1/needgo?access_token=" + token
    params = {
        "tileset": "needgo.app",
        "url": "mapbox://datasets/needgo/" + "cjuojgd9c01z632la84qa1v61",
        "name": "app"
    }

    print("LLEGA AQUI 2")

    print(params)
    try:
        print("intento")
        request = post(url, json=params)
        print("se hace request")
        print(request)
        response = request.text
        print(response)
    except RequestException:
        print("EXCEPTION")
        response = "Error saving record in mapbox"

    return response


scheduler.start()
