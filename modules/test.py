import requests
from pprint import pprint

from templates.text import TextTemplate

headers = {'Accept' : 'application/json', 'user_key': 'ada7140b071d43fe7ac36c260b854174', 'User-Agent': 'curl/7.35.0'}


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
            template_list=[TextTemplate(text=review["review"]['rating_text']+' - '+str(review["review"]['rating'])+'/5'+'\n'+review["review"]['review_text']).get_message() for review in data['user_review']]
            pprint(template_list)
            return template_list
    else:
        return TextTemplate('I\'m facing some issues, try again later').get_message()

if __name__ =='__main__':
    id= 300632
    pprint(get_reviews(id))