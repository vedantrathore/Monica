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
        pprint(result)
        action = result['action']
        parameters = result['parameters']
        if 'actionIncomplete' in result:
            actionIncomplete = result['actionIncomplete']
            if actionIncomplete is True:
                # print action
                # pprint(result['fulfillment']['speech'])
                return None, result['fulfillment']['speech']
        if action in src.__all__:
            # pprint(action)
            # pprint(parameters)
            return action, parameters
        else:
            # pprint(action)
            # pprint(result['fulfillment']['speech'])
            return action, result['fulfillment']['speech']
    except:
        pass
        # return None, {}

def search(input):
    action,parameters = process_query(input)
    if action in src.__all__:
        data = sys.modules['modules.src.' + action].process(action,parameters)
        if data['success'] == True:
            return data['output']
        else:
            if 'error_msg' in data:
                return data['error_msg']
            else:
                return TextTemplate('Something didn\'t work as expected! I\'ll report this to my authority.').get_message()
    elif action is not None:
        # print parameters
        return TextTemplate(str(parameters)).get_message()
    elif action is None and parameters is not None:
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
            template = GenericTemplate()
            for review in data["user_reviews"]:
                review = review["review"]
                template.add_element(title=review['rating_text']+' - '+review['rating']+'/5',subtitle=review['review_text'])
            return template.get_message()
    else:
        return TextTemplate('I\'m facing some issues, try again later').get_message()

def get_directions(id):
    print id
    return