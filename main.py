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
    # get the intent of the users message
    witresp = witbot.message(text)
    # get the intent and confidenceScore only if the condition is True
    if "intent" in witresp['entities'].keys():
        intents = witresp['entities']['intent'][0]['value']
        confidenceScore = witresp['entities']['intent'][0]['confidence']
        # call the func to respond to the user
        respond_to_user(witresp,intents,confidenceScore,recipient_id)
    else:
        show_error_message(recipient_id)

def respond_to_user(witresp,intents,confidenceScore,recipient_id):
    #if 'entities' in witresp.keys():
    intent_list = [intents]
    keys = witresp['entities'].keys()
    if 'greet' in intent_list:
    # sending some greetings
        send_greetings(recipient_id)
    elif 'showTacoLoc' in intent_list:
        # get_taco_shops() is called when the user requests for tacos. That's
        # when the showTacoLoc entitie is found
        get_taco_shops(recipient_id,keys)
        show_more_options(recipient_id)
    elif 'ShowMeme' in intent_list:
        bot.send_text_message(recipient_id,"Okay! This is what I found.👀🎞")
        send_funny_gif(recipient_id)
        # show the `show more` button and `not now` button
        reply_options = (["Show me MORE!😆","ShowMeme"],["I'm good🙂","nomeme"],)
        reply_payload = create_quickreply_payload(reply_options)
        send_quick_replies(recipient_id,"what next?",reply_payload)
    else:
        # show the options and an error message
        show_error_message(recipient_id)


def send_greetings(recipient_id):
    # sends random greetings to the user when the user responds with a greet-word
    greet_list = ["Hola Amigo","Oye Amigo","Hello","Hey","Hi"]
    Botresp = ", how can I help you?🤖🌮"
    message = "{}".format(greet_list[random.randint(0,len(greet_list)-1)]) + Botresp
    reply_options = (
                    ["Taco restuarants🍽🌮🍥","eating"],
                    ["Taco recipes📖🌮","ShowTacoRecipes"],
                    ["😄","ShowEmoji"],
                 )
    try:
        send_quick_replies(recipient_id,message,reply_options)
    except:
        bot.send_text_message(recipient_id,message)



def show_error_message(recipient_id):
    # this function shows the user some options
    reply_options = (["I want to eat😋","eating"],["read about tacos📖","reading"],["Make me laugh😆!!","ShowMeme"],["#TacosForever","something"])
    send_quick_replies(recipient_id,"Sorry, I didn't get you! Select something from the options below",reply_options)

def show_more_options(recipient_id):
    reply_options = (["food😋","eating"],["Top taco recipes📖","reading"],["Gifs🖼","ShowMeme"])
    send_quick_replies(recipient_id,"What do you want to do next?",reply_options)

# quick replies
def create_quickreply_payload(qk_payload):
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

def send_quick_replies(recipient_id,quick_reply_message,reply_options):
    # sends the quick reply button
    # automatically constructs the payload for the buttons from the list
    reply_payload = create_quickreply_payload(reply_options)
    botutils.send_quickreply(token = ACCESS_TOKEN,
        user_id = recipient_id,
        text = "{}".format(quick_reply_message),
        reply_payload = reply_payload,
    )

# functions for tacos
def get_taco_shops(recipient_id,keys):
    message = "Taco shops near you🌮🌮"
    bot.send_text_message(recipient_id, message)
    Show_taco_location(recipient_id,keys=keys)

def Show_taco_location(recipient_id,keys):
    # this function sends the taco shops near the user
    # zom api sends request to get all the taco shops
    if keys is None:
        return ""
    message = "tacocoo"
    bot.send_text_message(recipient_id, message)

# funny area
def send_funny_gif(recipient_id):
    # select a gif at random and send
    image_url_list = botutils.search_gifs(credentials['TENOR_API'],"taco")
    bot.send_image_url(
            recipient_id,
            image_url_list[random.randint(0,len(image_url_list)-1)]
    )

if __name__ == '__main__':
    app.run(debug=True,port=8080)
