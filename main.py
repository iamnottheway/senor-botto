from flask import Flask,request,render_template
from pymessenger.bot import Bot
from wit import Wit
from creds import credentials
import random
from zomatowrap import ZomatoApi
import botutils

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
            greet_list = ["Hola Amigo","Oye Amigo","Hello","Hey","Hi"]
            Botresp = ", how can I help you?🤖🌮"
            message = "{}".format(greet_list[random.randint(0,len(greet_list)-1)]) + Botresp
            bot.send_text_message(recipient_id, message)
        elif "taco" in keys:
            # show taco images and locations
            message = "This should calm you down🌮🌮"
            bot.send_text_message(recipient_id, message)
            Show_taco_location(recipient_id,keys=keys)
        elif "search_taco" in keys or "taco_shop" in keys:
            # show the taco places
            Show_taco_location(recipient_id,keys=keys)
        elif "meme" in keys:
            bot.send_text_message(recipient_id, "Okay! This is what I found.👀🎞")
            send_funny_gif(recipient_id)
            # show the show more button and no thanks button
            show_more_meme_payload = [
                {
                    "content_type":"text",
                    "title":"show more",
                    "payload":"meme"
                },
                {
                    "content_type":"text",
                    "title":"no thanks",
                    "payload":"nomeme"
                }
            ]
            botutils.send_quickreply(token = ACCESS_TOKEN,
                user_id = recipient_id,
                text = "what next?",
                reply_payload = show_more_meme_payload,
            )
        elif "nomeme" in keys:
            bot.send_text_message(recipient_id, "Okay cool! I'll make you laugh someother time")
        else:
            # show the options and an error message
            show_quick_replies(recipient_id,"Sorry, I didn't get you! Select something from the options below")


def show_quick_replies(recipient_id,quick_reply_message):
    # this is shown when the bot couldnt understand the user
    reply_payload = [
        {
            "content_type":"text",
            "title":"eat",
            "payload":"eating"
        },{
            "content_type":"text",
            "title":"read about tacos",
            "payload":"reading"
        },
        {
            "content_type":"text",
            "title":"memes",
            "payload":"meme"
        }
    ]
    botutils.send_quickreply(token = ACCESS_TOKEN,
        user_id = recipient_id,
        text = "{}".format(quick_reply_message),
        reply_payload = reply_payload,
    )

def Show_taco_location(recipient_id,keys):
    # this function sends the taco shops near the user
    # zom api sends request to get all the taco shops
    if keys is None:
        return ""
    message = "tacocoo"
    bot.send_text_message(recipient_id, message)

def send_funny_gif(recipient_id):
    # select a gif at random and send
    image_url_list = botutils.search_gifs(credentials['TENOR_API'],"taco")
    bot.send_image_url(recipient_id, image_url_list[random.randint(0,len(image_url_list)-1)])

if __name__ == '__main__':
    app.run(debug=True,port=8080)
