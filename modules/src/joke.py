from random import choice
from templates.button import ButtonTemplate
from templates.text import TextTemplate
import sys,os
import config,json


def process(action,parameter):
    output ={}
    try:
        # picks a random joke from a list of jokes and send it
        with open(config.JOKES_SOURCE_FILE) as jokes_file:
            jokes = json.load(jokes_file)
            jokes_list = jokes['jokes']
        joke = choice(jokes_list)
        template = ButtonTemplate(text=joke) # a text template for facebook messenger
        template.add_postback(title='One more!',payload='more!joke')
        #adding payload
        output['action'] = action
        output['success'] = True
        output['output'] = template.get_message()
    # for exiting gracefully
    except Exception as E:
        print E
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print exc_type, fname, exc_tb.tb_lineno
        error_message = 'I couldn\'t find any Joke '
        error_message += '\nPlease ask me something else, like:'
        error_message += '\n  - Tell me a Joke'
        error_message += '\n  - I\'m bored'
        error_message += '\n  - You are boring'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output

if __name__ == '__main__':
    print process('joke','parameter')