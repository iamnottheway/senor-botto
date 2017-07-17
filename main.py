from flask import Flask,request,render_template
from pymessenger.bot import Bot
from wit import Wit
from creds import credentials
import random
from zomatowrap import ZomatoApi

# import credential keys
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
VERIFY_TOKEN = credentials['VERIFY_TOKEN']
WIT_ACCESS_TOKEN = credentials['WIT_ACCESS_TOKEN']
ZOMATO_KEY = credentials['ZOMATO_API']

app = Flask(__name__)
witbot = Wit(access_token=WIT_ACCESS_TOKEN)
# set up messenger wrapper
bot = Bot(ACCESS_TOKEN)
# set up zomato api
zomApi = ZomatoApi(ZOMATO_KEY)

# landing page for the bot
@app.route('/')
def index():
    return render_template("index.html")

# verify fb's request with the token
# this is a one-time verification, so every time you open the page it'll show an error
# the best thing to cover it is to place a nice looking page.
@app.route('/bothook',methods=['GET'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            # let the invalid verify pass silently
            pass

# recieve messages and pass it to some function which parses it further
@app.route('/bothook',methods=['POST'])
def recieve_incoming_messages():
    # just chilling babe!
    if request.method == "POST":
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    if x['message'].get('text'):
                        user_message = x['message']['text']
                        # calling the parse message function to further parse the message
                        parse_user_message(recipient_id,user_message)
                else:
                    pass
        return "Success"

# this function detects the response type and sends a message
def parse_user_message(recipient_id,text):
    message = "I couldn't understand you!"
    witresp = witbot.message(text)
    if 'entities' in witresp.keys():
        keys = witresp['entities'].keys()
        if "greetings" in keys:
            greet_list = ["Hola Amigo","Oye Amigo","Hey","Hi"]
            message = "{}".format(greet_list[random.randint(0,len(greet_list)-1)])
            bot.send_text_message(recipient_id, message)
        elif "taco" in keys:
            # show taco images and locations
            message = "This should calm you down🌮🌮"
            bot.send_text_message(recipient_id, message)
        elif "search_taco" in keys or "taco_shop" in keys:
            # show the taco places
            #Show_taco_location(recipient_id,keys=keys)
        else:
            # show the chat-menu
            message = "I couldn't understand you!"
            bot.send_text_message(recipient_id, message)


def Show_taco_location(recipient_id,keys):
    # this function sends the taco shops near the user
    if keys is None:
        return ""

        #zom_resp = zomApi.GetResturantCollections()
        #gbtn_title = "Cake"#zom_resp['collections'][1]['title']
        #gbtn_imgurl = "http://www.primrose-bakery.co.uk/shop/content/images/thumbs/0000362_chocolate-layer-cake.jpeg"#zom_resp['collections'][1]['image_url']
        #gbtn_weburl = "somefood.com"#zom_resp['collections'][1]['url']
        # returns resturants in a city
        #bot.send_generic_message(recipient_id, taco_payload)

    if "best" in keys:
        message = "Here are the best taco places in town!🌮🌮"
        bot.send_text_message(recipient_id, message)
    else:
        message = "Here's what I found in your city🌮"
        bot.send_text_message(recipient_id, message)

    bot.send_generic_message(recipient_id,
        elements = [
           {
            "title":"Cake",
            "image_url":"http://www.primrose-bakery.co.uk/shop/content/images/thumbs/0000362_chocolate-layer-cake.jpeg",
            "subtitle":"We\'ve got the right cake for everyone.",
            "default_action": {
              "type": "web_url",
              "url": "www.eatcake.com",
              "messenger_extensions": true,
              "webview_height_ratio": "tall",
              "fallback_url": ""
            },
            "buttons":[
              {
                "type":"web_url",
                "url":"{}".format(gbtn_weburl),
                "title":"View in Website"
              },
            ]
          }
        ])


if __name__ == '__main__':
    app.run(debug=True,port=8080)
