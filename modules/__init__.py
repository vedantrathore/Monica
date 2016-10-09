import config
import os,json
from pprint import pprint
import apiai
import sys
from src import *
from templates.text import TextTemplate

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
        print parameters
        return TextTemplate(str(parameters)).get_message()
    elif action is None and parameters is not None:
        print TextTemplate(str(parameters)).get_message()
        return TextTemplate(str(parameters)).get_message()
    else:
        return TextTemplate('I\'m sorry; I\'m not sure I understand what you\'re trying to say .\nTry typing "help" or "request"').get_message()
