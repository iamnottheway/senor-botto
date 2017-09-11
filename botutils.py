

#  utility file for messenger bot

import requests
import json

def send_quickreply(token,user_id,text,reply_payload):
    # quick reply for messenger 
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
    requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        data=payload,
        headers={
            'Content-type': 'application/json'
        }
    )

def search_gifs(tenor_key,tag_str):
    # looks for tags on tenor
    data = {
        "tag":tag_str,
        "key":tenor_key
    }
    resp = requests.get("https://api.tenor.com/v1/search",data=data)
    gif_list = []
    print(resp.json()['results'][0]['tags'])
    for x in range(0,len(resp.json()['results'])-1):
        gif_image = resp.json()['results'][x]['media'][0]['tinygif']['url']
        gif_list.append(gif_image)
    return gif_list

def build_generic_elements(elements):
    """ arg format : ({
                        "element_data":[{"data":[title,img_url,sub_title,action_url]},]
                        "button_data":[{"data":[url,title]}]
                    })

    """
    element_list = []
    button_list = []
    len_element = len(elements['element_data'])
    len_button = len(elements['button_data'])

    for i in range(len_button):
        button_list.append({
            "type":"web_url",
            "url":elements['button_data'][i]['data'][0],
            "title":elements['button_data'][i]['data'][1],
        })

    for x in range(len_element):
        element_list.append({
            "title":elements['element_data'][x]['data'][0],
            "image_url":elements['element_data'][x]['data'][1],
            "subtitle":elements['element_data'][x]['data'][2],
            "default_action":{
                "type": "web_url",
                "url": elements['element_data'][x]['data'][3],
                "webview_height_ratio": "tall",
            },
            "buttons": button_list,
        })
    return element_list

def send_generic_buttons(token,user_id):
    params = {
        "access_token":token,

    }

    list_ele = ({
                        "element_data":[
                                        {"data":["Test","http://unsplash.it/200?random","Stuff","google.com"]},
                                        {"data":["Test1","http://unsplash.it/200?random","Stuff","google.com"]},
                                       ],
                        "button_data":[
                                         {"data":["google.com","click"]},
                                      ]
                    })
    elements = build_generic_elements(list_ele)
    data=json.dumps({
      "recipient":{
        "id":user_id
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements": elements,
          }
        }
      }
    })

    requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        data=data,
        headers={
            'Content-type': 'application/json'
        }
    )
