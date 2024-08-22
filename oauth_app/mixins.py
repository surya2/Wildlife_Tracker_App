from django.conf import settings
import requests
import json

def Directions(*args, **kwargs):
    lat_a = kwargs.get('lat_a')
    long_a = kwargs.get('long_a')
    lat_b = kwargs.get('lat_b')
    long_b = kwargs.get('long_b')

    origin = f'{lat_a},{long_a}'
    dest = f'{lat_b},{long_b}'

    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': dest,
            'key': settings.GOOGLE_MAPS_API_KEY
        }
    )

    directions = result.json()
    if directions['status'] == 'OK':
        route = directions['routes'][0]['legs'][0]
        origin = route['start_address']
        dest = route['end_address']
        dist = route['distance']['text']
        dur = route['duration']['text']

        direction_steps = [
            [
                step['html_instructions'],
                step['distance']['text'],
                step['duration']['text'],
                step['start_location'],
                step['end_location'],
                step['maneuver'],
            ] for step in route['steps'
            ]
        ]
    
        return {
            'origin': origin,
            'destination': dest,
            'distance': dist,
            'duration': dur,
            'direction_steps': direction_steps,
        }
    else:
        return "Map Directions Not Found"
    