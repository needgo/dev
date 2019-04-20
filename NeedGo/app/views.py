from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import datetime
import time
from geojson import Feature, Point, FeatureCollection
import json
from .mapbox_manager import create_mapbox



# Create your views here.
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def index(request):
    return render(request, 'index.html')


def check_types(features):

    map= {["LineString", "LineString"]: "MultiLineString",
          ["Point", "Point"]: "MultiPoint",
          ["Polygon", "Polygon"]: "MultiPolygon",
          ["LineString"]: "LineString",
          ["Point"]: "Point",
          ["Polygon"]: "Polygon"}

    key= []
    for feature in json.loads(features)['features']:
        key.append(feature['geometry']['type'])

    return map.get(key)

@csrf_exempt
@transaction.atomic
def save_card(request):
    date = request.POST.get('date')
    title = request.POST.get('title')
    description = request.POST.get('description')
    duration = request.POST.get('duration')
    geojson = request.POST.get('geojson')
    hour = request.POST.get('hour')

    check = check_form(request)
    if check != True:
        return check

    for feature in json.loads(geojson)['features']:
        feature['properties']['hour'] = hour
        feature['properties']['duration'] = duration
        feature['properties']['title'] = title
        feature['properties']['description'] = description
        feature['properties']['date'] = date
        create_mapbox(feature)

    return JSONResponse("", status=200)



#Auxiliary methods
def validate(date_text):
    result= True
    try:
        date= datetime.datetime.strptime(date_text, '%Y-%m-%d')
        today= datetime.datetime.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')

        if date < today:
            result= False
    except ValueError:
        result= False
    return result

def is_json(myjson):
    result= True
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        result= False
    return result

def check_form(request):
    date = request.POST.get('date')
    title = request.POST.get('title')
    description = request.POST.get('description')
    duration = request.POST.get('duration')
    geojson = request.POST.get('geojson')
    hour = request.POST.get('hour')

    #Check title
    if title == None or title.strip() == "":
        return JSONResponse("You must especify the title", status=400)
    elif len(title) > 200:
        return JSONResponse("The maximum length of title is 200 characters", status=400)

    # Check description
    if description == None or description.strip() == "":
        return JSONResponse("You must especify the description", status=400)
    elif len(description) > 500:
        return JSONResponse("The maximum length of description is 500 characters", status=400)

    # Check duration
    if duration == None or duration.strip() == "":
        return JSONResponse("You must especify the description", status=400)
    elif not duration.isdigit():
        return JSONResponse("The duration must be a number", status=400)
    elif int(duration) < 1:
        return JSONResponse("The minimum duration is 1 minute", status=400)

    #Check hour
    if hour == None or hour.strip() == "":
        return JSONResponse("You must especify the hour", status=400)
    numbers = hour.split(":")
    if len(numbers) != 2 or not numbers[0].isdigit() or not numbers[1].isdigit() or len(numbers[0])!=2 or len(numbers[1])!=2 or  int(numbers[0]) < 0 or int(numbers[0]) > 23 or int(numbers[1]) < 0 or int(numbers[1]) > 59:
        return JSONResponse("The hour format is not correct", status=400)

    # Check date
    if date == None or date.strip() == "":
        return JSONResponse("You must especify the date", status=400)
    elif not validate(date):
        return JSONResponse("The date must be a correct date in the future", status=400)

    # Check geojson
    if geojson == None or geojson.strip() == "":
        return JSONResponse("You can't modify the form", status=400)
    elif not is_json(geojson):
        return JSONResponse("The geojson is not a valid json", status=400)

    geojson = json.loads(geojson)

    if not isinstance(json.dumps(geojson), list):
        geojsonObject = Feature(geojson['features'][0])
    elif len(json.dumps(geojson)) == 2:
        geojsonObject = FeatureCollection([geojson['features'][0], geojson['features'][1]])

    else:
        return JSONResponse("The number of shapes is bigger than 2", status=400)


    if not geojsonObject.is_valid:
        return JSONResponse("The Geojson is not valid", status=400)


    return True
