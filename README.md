# Monica
[![Gitter Chat](http://img.shields.io/badge/chat-online-brightgreen.svg)](https://gitter.im/monicabot/Lobby)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

## About

Monica is a facebook messenger bot which uses Natural language processing and machine learning intelligence to search restaurants based on user inputs like location and cuisine with the of Zomato Api.

## Testing

The bot is live on : https://monicabot.herokuapp.com

To chat with the bot you should be added as a test user. 
Goto the Bot monica facebook page [here](https://www.facebook.com/Bot-Monica-158214041302319/) and comment to be a  test user

You can now test the bot using queries like 
* Search for chinese restaurants in Banglore under 1000 Rs
* I'm Hungry
* Is there any place to eat in guwahati?
The bot not only supports restaurant searching but can also hold natural conversations like
* Hey!
* What's up?
* Where are you from?
* Do you have friends?
* Tell me a joke?
* Fact?
* Tell a quote

## Development  

```
$ git clone https://github.com/vedantrathore/Monica.git \\clone the repo
$ cd Monica/
$ pip install -r requirements.txt \\Install all the dependencies
$ python runserver.py \\Start the server
```
goto ```http://127.0.0.1:5000/search/?q=<<Your query>>/``` to see the results of your query
