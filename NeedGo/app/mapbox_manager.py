from requests import post, put, delete
from requests.exceptions import RequestException


def create_mapbox(geojson):
    # Mapbox configuration

    token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

    print(geojson)
    url= "https://api.mapbox.com/datasets/v1/needgo/cjuojgd9c01z632la84qa1v61/features/"+str(geojson['id'])+"?access_token="+token
    params = geojson



    try:
        request= put(url, json= params)
        response = request.text
    except RequestException as e:
        print(e)
        response = "Error saving record in mapbox"

    return response


def delete_mapbox(idFeature):
    # Mapbox configuration
    token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

    url = "https://api.mapbox.com/datasets/v1/needgo/cjuojgd9c01z632la84qa1v61/features/" + str(idFeature) + "?access_token=" + token

    try:
        request = delete(url)
        response = request.text
    except RequestException:
        response = "Error deleting record in mapbox"

    return response


def update_mapbox():

    # Mapbox configuration
    token = "sk.eyJ1IjoibmVlZGdvIiwiYSI6ImNqdXBhcjFycDMyYWs0NHFqZW91M24xbnAifQ.q89AEpZGKAYihE0wRRMnQQ"

    url = "https://api.mapbox.com/uploads/v1/needgo?access_token="+token
    params = {
        "tileset": "needgo.cjuojgd9c01z632la84qa1v61-0fykf",
        "url": "mapbox://datasets/needgo/cjtke1edi02q02wn5kjd9en24",
        "name": "cjuojgd9c01z632la84qa1v61-0fykf"
    }

    try:
        request = post(url, json=params)
        response = request.text
    except RequestException:
        response = "Error saving record in mapbox"

    return response
