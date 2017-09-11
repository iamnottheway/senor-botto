

#  utility file for messenger bot

import requests
import json
from credentials import credentials


token = credentials['ACCESS_TOKEN']

# show the `get started` button
def GetStartedButton_createBtn():
    params = {
        "access_token":token,
    }
    payload = json.dumps({
            "get_started":{
                        "payload":"@get_started"
            }
    })
    
    resp = requests.post(
                    "https://graph.facebook.com/v2.6/me/messenger_profile",
                    params=params,
                    data=payload,
                    headers={
                        'Content-type': 'application/json'
                    }
    )
    return resp.json()



# get the payload from the get started button
def GetStartedButton_getPayload():
    params = {
        "access_token":token,
    }
    requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=get_started",params=params)

# delete the `get started` button
def GetStartedButton_deleteBtn():
    params = {
        "access_token":token,
    }
    payload = {
            "fields":[
                    "get_started"
            ]
    }
    resp = requests.delete(
                    "https://graph.facebook.com/v2.6/me/messenger_profile",
                    params=params,data=payload,
                    headers={'Content-type':'application/json'}
    )
    return resp.status_code



# quick reply button function
def QuickReply_Send(token,user_id,text,reply_payload):
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



# quick replies
def QuickReply_CreatePayload(qk_payload):
    # this function constructs and returns a payload for the the quick reply button payload
    # pass in a tuple-of-list / list-of-lists
    # example : (['title1','payload'],['title2','payload'])
    quick_btns = []
    for i in range(len(qk_payload)):
        quick_btns.append(
            {
                "content_type":"text",
                "title":qk_payload[i][0],
                "payload":qk_payload[i][1],
            }
        )
    return quick_btns

def QuickReply_SendButtons(recipient_id,quick_reply_message,reply_options):
    # sends the quick reply button
    # automatically constructs the payload for the buttons from the list
    reply_payload = QuickReply_CreatePayload(reply_options)
    QuickReply_Send(token = token,
        user_id = recipient_id,
        text = "{}".format(quick_reply_message),
        reply_payload = reply_payload,
    )



def TypingIndicator_Send(recipient_id,message_state):
    # this function sends the typing indicator to the user
    # message_state is the state where the bot is typing, has seen the message or has stopped typing
    # states : mark_seen,typing_on,typing_off
    params = {
        "access_token":token,
    }
    payload = {
      "recipient":{
            "id":recipient_id,
        },
      "sender_action":message_state,
    }
    requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        data=payload,
        headers={
            'Content-type': 'application/json'
        }
    )


# send video url to the user
def VideoUrl_Send(recipient_id,vid_url):
    params = {
        "access_token":token,
    }
    payload = {
      "recipient":{
            "id":recipient_id,
    },
    "message":{
        "attachment":{
          "type":"video",
          "payload":{
            "url":vid_url,
          }
        }
      }
    }
    requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        data=payload,
        headers={
            'Content-type': 'application/json'
        }
    )

def build_generic_elements(elements):
    """ arg format :({
                        "element_data":[{"data":[title,img_url,sub_title,action_url]},]
                        "button_data":[{"data":[url,title]}]
                    })

    """
    element_list = []
    button_list = []
    len_element = len(elements['element_data'])
    len_button = len(elements['button_data'])
    
    # constructs the button payload
    for i in range(len_button):
        button_list.append({
            "type":"web_url",
            "url":elements['button_data'][i]['data'][0],
            "title":elements['button_data'][i]['data'][1],
        })

    # constructs the generic elements payload
    # doesnt show all the location. Problem with the index maybe
    print(elements['element_data'][0][0])
    for x in range(len_element):
        element_list.append({
            "title":elements['element_data'][x][x]['data'][0],
            "image_url":elements['element_data'][x][x]['data'][1],
            "subtitle":elements['element_data'][x][x]['data'][2],
            "default_action":{
                "type": "web_url",
                "url": elements['element_data'][x][x]['data'][3],
                "webview_height_ratio": "tall",
            },
            "buttons": button_list,
        })
    return element_list

def generic_button_send(user_id,element_payload):
    params = {
        "access_token":token,

    }


    # builds the payload for elements in JSON format
    elements = build_generic_elements(element_payload)
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


def Persistant_menu():
    params = {
        "access_token":token,
    }
    payload = json.dumps({
        "persistent_menu":[
        {
          "locale":"default",
          "composer_input_disabled":True,
          "call_to_actions":[
            {
              "title":"Start over🤖",
              "type":"postback",
              "payload":"@get_started"
            },
          ]
        },
        {
          "locale":"zh_CN",
          "composer_input_disabled":False,
        }
       ]
    })
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messenger_profile",
        params=params,
        data=payload,
        headers={
            'Content-type': 'application/json'
        }
    )
    return resp.json()


def Ask_user_location(recipient_id):
    """ Sends a request for a quick reply btn asking users loc

    """
    params = {
        "access_token":token,

    }
    data=json.dumps({

        "recipient":{
            "id":"{}".format(recipient_id)
          },
          "message":{
            "text": "Where do you live?",
            "quick_replies":[
              {
                "content_type":"location"
              }
            ]
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


def payment(user_id):
    params = {
        "access_token":token,
    }
    payload = json.dumps({ 
        "recipient":{
            "id":user_id
        },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":[
               {
                "title":"DC Hunt",
                "image_url":"https://www.google.co.in/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
                "subtitle":"Hunt it",
                "default_action": {
                  "type": "web_url",
                  "url": "https://www.google.com",
                  "webview_height_ratio": "tall",
                  "fallback_url": "https://www.google.com"
                },
                "buttons":[{
                      "type":"payment",
                      "title":"buy",
                      "payload":"@payed",
                      "payment_summary":{
                        "currency":"USD",
                        "payment_type":"FIXED_AMOUNT",
                        "is_test_payment" : True, 
                        "merchant_name":"DC Hunt",
                        "requested_user_info":[
                          "shipping_address",
                          "contact_name",
                          "contact_phone",
                          "contact_email"
                        ],
                        "price_list":[
                          {
                            "label":"Subtotal",
                            "amount":"29.99"
                          },
                          {
                            "label":"Taxes",
                            "amount":"2.47"
                          }
                        ]
                    }
                }]      
              }
            ]
          }
        }
        }

    })
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        data=payload,
        headers={
            'Content-type': 'application/json'
        }
    )
    return resp
    
