import json

from flask import Flask, render_template, request
import requests
from flask_cors import CORS

from geolib import geohash

URL_TicketMaster = "https://app.ticketmaster.com/discovery/v2/events.json"
# URL_Google = "https://maps.googleapis.com/maps/api/geocode/json"
# inputs TM
# geohash = geohash.encode('70.2995', '-27.9993', 7)
app = Flask(__name__)
CORS(app)


@app.route('/events', methods=['GET'])
def get_events():
    geo_point = '9q5cs'
    unit = 'miles'
    apikey = 'EnterYourKey'
    
    all_args = request.args.to_dict()
    keyword = all_args.get('keyword')
    radius = all_args.get('distance')
    category = all_args.get('category')
    
    if category == "Music":
        segment_id = "key"
    if category == "Sports":
        segment_id = "key"
    if category == "Arts & Theatre":
        segment_id = "key"
    if category == "Film":
        segment_id = "key"
    if category == "Miscellaneous":
        segment_id = "key"
    if category == "default":
        segment_id = ""
    par = {'apikey': apikey, 'geo_point': geo_point, 'radius': radius, 'segment_id': segment_id, 'unit': unit,
           'keyword': keyword}

    # google = requests.get(url=URL_Google, params=g_par)
    ticketmaster = requests.get(url=URL_TicketMaster, params=par)

    data_tm = ticketmaster.json()
    # data_g = google.json()
    events = data_tm['_embedded']['events']
    # name = data_tm['_embedded']['events'][0]['name']
    # date = data_tm['_embedded']['events'][0]['sales']['public']['startDateTime']

    tmp = []

    for event in events:
        name = event['name']
        icon = event['images'][0]['url']
        date = event['dates']['start']['localDate']
        # time = event['dates']['start']['localTime']
        genre = event['classifications'][0]['segment']['name']
        venue = event['_embedded']['venues'][0]['name']
        result = dict()
        result['name'] = name
        result['date'] = date
        # result['time'] = time
        result['genre'] = genre
        result['venue'] = venue
        result['icon'] = icon
        tmp.append(result)

    return json.dumps(tmp)


if __name__ == '__main__':
    app.run('0.0.0.0', 5009)
