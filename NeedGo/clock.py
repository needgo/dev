import os
import django
from requests import get, post, delete
from requests.exceptions import RequestException
from datetime import datetime
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeedGo.settings')
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', id='update_mapbox_function_id', seconds=60)
def update_mapbox_function():


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


    try:
        request = post(url, json=params)

        response = request.text
        print(response)

    except RequestException:

        response = "Error saving record in mapbox"

    return response


@scheduler.scheduled_job('cron', id='delete_mapbox_function', hour=0)
def delete_mapbox_function(request):
    # Mapbox configuration
    token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

    url = "https://api.mapbox.com/datasets/v1/needgo/cjuojgd9c01z632la84qa1v61/features/" + "?access_token=" + token

    try:
        request = get(url)
        response = json.loads(request.text)

        for feature in response['features']:
            featureDateString = feature['properties']['date']+" "+feature['properties']['hour']+":00"
            featureDate = datetime.strptime(featureDateString, '%Y-%m-%d %H:%M:%S')

            if featureDate < datetime.now():
                # Mapbox configuration
                token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

                url = "https://api.mapbox.com/datasets/v1/needgo/cjuojgd9c01z632la84qa1v61/features/" + str(
                    feature['id']) + "?access_token=" + token

                try:
                    request = delete(url)
                    response = request.text
                except RequestException:
                    response = "Error deleting record in mapbox"

    except RequestException:
        response = "Error deleting record in mapbox"

    return response


scheduler.start()
