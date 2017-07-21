

#  utility file for messenger bot

import requests
import json

def send_quickreply(token,user_id,text,reply_payload):

    params = {
        "access_token":token,

    }
    payload = json.dumps({
      "recipient":{"id":user_id,},
      "message":{
        "text":"{}".format(text),
        "quick_replies":reply_payload,
      }
    })
    requests.post("https://graph.facebook.com/v2.6/me/messages",params=params,
                data=payload,headers={'Content-type': 'application/json'})

def search_gifs(tenor_key,tag_str):
    # looks for tags on tenor
    data = {
        "tag":tag_str,
        "key":tenor_key
    }
    resp = requests.get("https://api.tenor.com/v1/search",data=data)
    return resp.json()
