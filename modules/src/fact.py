from random import choice
from templates.button import ButtonTemplate
from templates.text import TextTemplate
import sys,os
import config,json


def process(action,parameter):
    output ={}
    try:
        with open(config.FACTS_SOURCE_FILE) as facts_file:
            facts = json.load(facts_file)
            facts_list = facts['facts']
        fact = choice(facts_list)
        template = ButtonTemplate(text=fact)
        template.add_postback(title='One more!',payload='more!fact')
        output['action'] = action
        output['success'] = True
        output['output'] = template.get_message()
    except Exception as E:
        print E
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print exc_type, fname, exc_tb.tb_lineno
        error_message = 'I couldn\'t find any fact '
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - Tell me a fact'
        error_message += '\n  - I\'m demotivated'
        error_message += '\n  - I want a fact'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output

if __name__ == '__main__':
    print process('fact','parameter')