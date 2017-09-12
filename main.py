from flask import Flask
from flask import request
from pymessenger.bot import Bot
from credentials import credentials
import get_food_data  # yelp
import botutils


# import credential keys
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
VERIFY_TOKEN = credentials['VERIFY_TOKEN']


app = Flask(__name__)
# set up messenger wrapper
bot = Bot(ACCESS_TOKEN)


x = botutils.GetStartedButton_createBtn()
botutils.Persistant_menu()

@app.route('/')
def index():
    return 'ok'
# verify fb's request with the token
# this is a one-time verification, so every time you open the page it'll show an error
# the best thing to cover it is to place a nice looking page.
@app.route('/testbot',methods=['GET'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            # let the invalid verify pass silently
            pass

location = "none"
# recieve messages and pass it to some function which parses it further
@app.route('/testbot',methods=['POST'])
def recieve_incoming_messages():
    global location
    # just chilling babe!
    if request.method == "POST":
        output = request.get_json()
        # for normal text messages
        # get the recipient id and user message from the JSON response
        user_payload = "@none"
        recipient_id = "@none"
        user_message = ""

        for event in output['entry']:
            if event.get('messaging'):
                messaging = event['messaging']
                for x in messaging:
                    if x.get('message'):
                        recipient_id = x['sender']['id']
                        if x['message'].get('text'):
                            user_message = x['message']['text']
                        if x['message'].get('quick_reply'):
                            user_payload = x['message']['quick_reply']['payload']
                        if x['message'].get('attachments'):
                            if x['message']['attachments'][0].get('payload'):
                                if x['message']['attachments'][0]['payload'].get('coordinates'):
                                    location = x['message']['attachments'][0]['payload']['coordinates']
                    if x.get('postback'):  # for postback getstarted button
                        recipient_id = x['sender']['id']
                        if x['postback'].get('payload'):
                            user_payload = x['postback']['payload']
        respond_back(recipient_id, user_payload,user_message)
    return "Success"


def respond_back(recipient_id,user_payload,user_message):
    """
    """
    global location
    if location is not "none":
        # if location has some value set the new payload
        # so that the function is executed
        user_payload = "@ShowTaco"



def Show_getStartedBtn(user_id):
    global location
    location = "none"
    intro_message = """ Hola amigo! I'm Senor botto🌮. I can show you some of the best taco restuarants in your city🍽! Or tell you a joke or show something funny.
                    """
    bot.send_text_message(user_id,intro_message)
    reply_options = [("I want to eat","@taco"),("Make me laugh","@joke")]
    botutils.QuickReply_SendButtons(user_id, "What do you want to do?👇", reply_options)

def AskUserLocation(recipient_id):
    botutils.Ask_user_location(recipient_id)

def SearchTacoVendor(recipient_id):
    element_data_list = []
    global location # location is a dict
    food_data = get_food_data.yelp_search(coords=(location['long'],location['lat'])) # init with key. Done internally
    packed_results = get_food_data.get_res_info(food_data)
    if len(packed_results) == 0:
        bot.send_text_message(recipient_id,"Couldn't find anything in your area🍁.")
        location = "none"
    else:
        food_data_list = []
        # building the restaurant data here and packing it into a list
        for restaurant_num in range(len(packed_results)):
            # combines cost and ratings in a string. Displayed with address
            sub_detail_str = "{0}, Ratings:{1}".format(packed_results[restaurant_num][4],
                                                        packed_results[restaurant_num][1],
                )
            # the data is appended to the list
            food_data_list.append({"data":(packed_results[restaurant_num][0],
                                           packed_results[restaurant_num][3],
                                           sub_detail_str,
                                           "www.google.com"
                )})

        bot.send_text_message(recipient_id,"Here's what I've found")
        ele_payload = ({
                            "element_data":food_data_list,
                            "button_data":[{"data":["www.google.com","Learn more🌮"]}]
                        })
        botutils.generic_button_send(recipient_id,ele_payload)


def ignore_func(recipient_id):
    r = botutils.get_payment(recipient_id)
    print(r.json())



if __name__ == '__main__':
    app.run(debug=True,port=8080,threaded=True)
