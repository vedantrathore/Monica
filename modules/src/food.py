from pprint import pprint
import sys,os
import requests, json
from templates.button import *
from templates.generic import *

headers = {'Accept': 'application/json', 'user_key': 'ada7140b071d43fe7ac36c260b854174', 'User-Agent': 'curl/7.35.0'}


def get_location(location):
    key = "AhuYVYvwc666R0W_9dNUo9sTq1YjyzIzU4QdRD_7wB1qdb75BwoZj4Rg7tgpyLM9"
    url = "http://dev.virtualearth.net/REST/v1/Locations/" + location + "?inclnb=1&o=json&key=" + key
    request = requests.get(url)
    # pprint(request.text)
    response = json.loads(request.text)
    result = response['resourceSets'][0]['resources'][0]['point']['coordinates']
    return result[0], result[1]


def get_template(restaurants):
    template = GenericTemplate()
    for restaurant in restaurants:
        template.add_element(title=restaurant['name']+'| Rating : '+str(restaurant['rating'])+'/5', subtitle='Cost for 2 : '+str(restaurant['budget'])+' |  Locality: '+restaurant['locality'],item_url=restaurant['url'],
                             image_url=restaurant['image_url'],buttons=[
                        {
                           "type": "web_url",
                           "url": restaurant['url'],
                           "title": "Visit Website"
                       },
                       {
                           "type": "postback",
                           "title": "Get Reviews",
                           "payload": "get_reviews!"+restaurant['id']
                       },
                       {
                           "type": "postback",
                           "title": "Get Directions",
                           "payload": "get_directions!"+restaurant['id']
                       }])
    pprint(template)
    return template


def process(action, parameters):
    output = {}
    if parameters['geo-city'] is None or parameters['number-integer'] is None:
        return output
    lat, lon = get_location(parameters['geo-city'])
    url = 'https://developers.zomato.com/api/v2.1/search?count=10&sort=rating&order=desc' + '&lat=' + str(
        lat) + '&lon=' + str(lon)
    if parameters['cuisines'] is not None:
        url += "&cuisines=" + parameters['cuisines']
    try:
        r = requests.get(url, headers=headers)
        restaurants = []
        if r.status_code != 200:
            print "Api Issues"
            return
        if len(r.json()['restaurants']) <= 0:
            print "Api Issues"
            return
        for res in r.json()['restaurants']:
            rest = {'budget': res['restaurant']['currency'] + ' ' + str(res['restaurant']['average_cost_for_two']),
                    'id': res['restaurant']['id'], 'name': res['restaurant']['name'], 'url': res['restaurant']['url'],
                    'location_lat': res['restaurant']['location']['latitude'],
                    'location_lon': res['restaurant']['location']['longitude'],
                    'rating': res['restaurant']['user_rating']['aggregate_rating'],
                    'locality': res['restaurant']['location']['locality'], 'image_url': res['restaurant']['thumb']}
            restaurants.append(rest)
        # pprint(restaurants)
        template1 = get_template(restaurants)
        # pprint(template1.get_message())
        output['action'] = action
        output['output'] = template1.get_message()
        output['success'] = True
    except Exception as E:
        print E
        exc_type,exc_obj,exc_tb=sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print exc_type,fname,exc_tb.tb_lineno
        error_message = 'I couldn\'t find any Restaurant matching your query.'
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - Some restaurants in guwahati under 1000 Rs'
        error_message += '\n  - Any place to eat in Mumbai'
        error_message += '\n  - I\'m Hungry'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output


if __name__ == '__main__':
    pass
