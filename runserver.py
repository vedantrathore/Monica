import config
from flask import render_template,Flask, request
import json
import os
import requests
import modules
from pprint import pprint

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', config.VERIFY_TOKEN)

app = Flask(__name__)


@app.route('/')
def about():
    return render_template('index.html')


@app.route('/process/')
def process():
    return json.dumps(modules.process_query(request.args.get('q')))


@app.route('/search/')
def search():
    return json.dumps(modules.search(request.args.get('q')))


@app.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json(force=True)
        pprint(data)
        messaging_events = data['entry'][0]['messaging']
        for event in messaging_events:
            sender = event['sender']['id']
            if 'message' in event and 'text' in event['message']:
                text = event['message']['text']
                payload = {
                    'recipient': {
                        'id': sender
                    },
                    'message': modules.search(text)
                }
                # pprint(payload)
                r = requests.post('https://graph.facebook.com/v2.8/me/messages',
                                  params={'access_token': ACCESS_TOKEN},
                                  json=payload)
            elif 'postback' in event:
                postback = event['postback']['payload'].split('!')[0]
                id = event['postback']['payload'].split('!')[1]
                if postback == "get_reviews":
                    review_list = modules.get_reviews(id)
                    for review in review_list:
                        payload = {
                            'recipient': {
                                'id': sender
                            },
                            'message': review
                        }
                        # pprint(payload)
                        r = requests.post('https://graph.facebook.com/v2.8/me/messages',
                                          params={'access_token': ACCESS_TOKEN},
                                          json=payload)
                elif postback == "get_directions":
                    payload = {
                        'recipient': {
                            'id': sender
                        },
                        'message': modules.get_directions(id)
                    }
                    # pprint(payload)
                    r = requests.post('https://graph.facebook.com/v2.8/me/messages',
                                      params={'access_token': ACCESS_TOKEN},
                                      json=payload)
                elif postback == "more":
                    payload = {
                        'recipient': {
                            'id': sender
                        },
                        'message': modules.search(id)
                    }
                    # pprint(payload)
                    r = requests.post('https://graph.facebook.com/v2.8/me/messages',
                                      params={'access_token': ACCESS_TOKEN},
                                      json=payload)
        return ''
    elif request.method == 'GET':  # Verification
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return 'Error, wrong validation token'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
    # while True:
    #     i= raw_input(">")
    #     pprint(modules.search(i))
    # id = 300632
    # a= (modules.search())