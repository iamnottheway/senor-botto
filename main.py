from flask import Flask,request
from pymessenger.bot import Bot
from wit import Wit
from creds import credentials
import random

# import credential keys
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
VERIFY_TOKEN = credentials['VERIFY_TOKEN']
WIT_ACCESS_TOKEN = credentials['WIT_ACCESS_TOKEN']

app = Flask(__name__)
witbot = Wit(access_token=WIT_ACCESS_TOKEN)
# set up messenger wrapper
bot = Bot(ACCESS_TOKEN)
# landing page for the bot
@app.route('/')
def index():
    return "ok"

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
        else:
            # send a button message, so that the user will have options
            btn_payload = [
                {
                    "type":"postback",
                    "title":"say Hola",
                    "payload":"USER_DEFINED_PAYLOAD"
                 },{
                    "type":"postback",
                    "title":"Taco places in town!",
                    "payload":"USER_DEFINED_PAYLOAD"
                  },{
                    "type":"postback",
                    "title":"Taco recipies",
                    "payload":"USER_DEFINED_PAYLOAD"
                  }

            ]
            bot.send_button_message(recipient_id = recipient_id,
                    text = "Select from here amigo",
                    buttons = btn_payload
            )

if __name__ == '__main__':
    app.run(debug=True,port=8080)
