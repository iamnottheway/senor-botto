

import requests

def send_quickreply(fb_token,user_id,text,reply_payload):
    # url parameters
    headers = {
        "access_token":"{}".format(fb_token),

    }
    # quick replies payload
    payload = {
      "recipient":{
        "id":"{}".format(user_id)
      },
      "message":{
        "text":"{}".format(text),
        "quick_replies":reply_payload,
      }
    }
    url = "https://graph.facebook.com/v2.6/me/messages"
    requests.post(url,headers=headers,data=payload)

