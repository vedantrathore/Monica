import config
import os,json,requests
from pprint import pprint
import apiai
import sys
from src import *
from templates.text import TextTemplate
from templates.generic import GenericTemplate

headers = {'Accept' : 'application/json', 'user_key': 'ada7140b071d43fe7ac36c260b854174', 'User-Agent': 'curl/7.35.0'}

API_AI_ACCESS_TOKEN = os.environ.get('API_AI_ACCESS_TOKEN', config.API_AI_ACCESS_TOKEN)
r = apiai.ApiAI(API_AI_ACCESS_TOKEN)


def process_query(input):
    try:
        request = r.text_request()
        request.query = input
        response = json.loads(request.getresponse().read())
        result = response['result']
        # pprint(result)
        action = result['action']
        parameters = result['parameters']
        if 'actionIncomplete' in result:
            actionIncomplete = result['actionIncomplete']
            if actionIncomplete is True:
                return 'none', result['fulfillment']['speech']
        if action in src.__all__:
            return action, parameters
        else:
            # pprint(action)
            # pprint(result['fulfillment']['speech'])
            return action, result['fulfillment']['speech']
    except:
        pass
        # return None, {}

def search(input):
    action, parameters = process_query(input)
    if action in src.__all__:
        data = sys.modules['modules.src.' + action].process(action,parameters)
        if data['success']:
            return data['output']
        else:
            if 'error_msg' in data:
                return data['error_msg']
            else:
                return TextTemplate('Something didn\'t work as expected! I\'ll report this to my authority.').get_message()
    elif action is not None:
        # print parameters
        return TextTemplate(str(parameters)).get_message()
    elif action is 'none' and parameters is not None:
        # print TextTemplate(str(parameters)).get_message()
        return TextTemplate(str(parameters)).get_message()
    else:
        return TextTemplate('I\'m sorry; I\'m not sure I understand what you\'re trying to say .\nTry typing "help" or "request"').get_message()


def get_reviews(id):
    url = "https://developers.zomato.com/api/v2.1/reviews?res_id=%s&count=5" % (id)
    try:
        response = requests.get(url, headers=headers)
    except:
        return TextTemplate('I\'m facing some issues, try again later').get_message()
    if response.status_code == 200:
        data = response.json()
        count = data["reviews_count"]
        if count == 0:
            return TextTemplate('Sorry, no reviews are available').get_message()
        else:
            template_list = []
            for review in data['user_reviews']:
                template_list.append({'text': review["review"]['rating_text'] + ' - ' + str(review["review"]['rating']) + '/5' + '\n' +
                         review["review"]['review_text']})
            pprint(template_list)
            return template_list
    else:
        return TextTemplate('I\'m facing some issues, try again later').get_message()


def get_directions(id):
    url='https://developers.zomato.com/api/v2.1/restaurant?res_id='+id
    try:
        response = requests.get(url, headers=headers)
    except:
            return TextTemplate('I\'m facing some issues, try again later').get_message()
    if response.status_code == 200:
        data = response.json()
        lat = data['location']['latitude']
        lon = data['location']['longitude']
        location = 'http://www.google.com/maps/place/'+lat+','+lon
        return TextTemplate('Here you go! :)'+'\n\n'+location).get_message()
    else:
        return TextTemplate('I\'m facing some issues, try again later').get_message()
