from templates.text import TextTemplate
import sys, os

# Sending help query subroutine
def process(action, parameter):
    output = {}
    help_message = "Hello I'm Monica Geller Bing, I am here to help you find great restaurants with the help of my skills :)"
    help_message += "\nSearch queries like"
    help_message += "\n  - Search for hotels in Banglore"
    help_message += "\n  - I wanna eat some chinese food"
    help_message += "\n  - I'm hungry"
    help_message += "\n  - Show me something to eat under 1000 Rs"
    help_message += "\n  - Tell me a joke"
    help_message += "\n  - I want a famous quote"
    help_message += "\n  - Some facts?"
    help_message += "\n  - I'm bored"
    try:
        template = TextTemplate(help_message)
        output['action'] = action
        output['success'] = True
        output['output'] = template.get_message()
    except Exception as E:
        print E
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print exc_type, fname, exc_tb.tb_lineno
        output['error_msg'] = TextTemplate(help_message).get_message()
        output['success'] = False
    return output


if __name__ == '__main__':
    print process('joke', 'parameter')
