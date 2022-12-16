from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
from env import *
from machine import *
from geopy.geocoders import Nominatim



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)
user = ""
target = 0



LineBot_api = LineBotApi(linebotapi)
handler = WebhookHandler(linehandler)

class elevator(db.Model):
    __tablename__ = 'elevators'
    sid = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    date = db.Column(db.Date)
    live = db.Column(db.Boolean)
    
    def __init__(self,name,date):
        self.name = name,
        self.date = date,
        self.live = True

@app.route('/insert')
def insert():
    name = "test"
    date = datetime.date(2022,12,4) 
    student = elevator(name,date)
    db.session.add(student)
    db.session.commit()
    return "success"

@app.route('/')
def create():
    db.create_all()
    return "connect success"

@app.route('/callback', methods=[ 'POST' ])
def callback():
    print("test")
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        #insert()
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort (400)
    return 'OK'

@handler.add (MessageEvent, message=TextMessage)
def handle_message (event):
    # LineBot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
    print("message")
    
    split_message = event.message.text.split(' ')
    if len(split_message) == 1:
        batman.trigger(split_message[0]) 
    if len(split_message) == 2:
        batman.trigger(split_message[0],split_message[1])
    if len(split_message) == 3:
       batman.trigger(split_message[0],split_message[1],split_message[2]) 
        
    #print(split_message[0])
    # batman.trigger(split_message[0])
    #print("next")
    #print(batman.msg)
    if(batman.willImg == 0):
        LineBot_api.reply_message(event.reply_token, TextSendMessage(text=batman.msg)) 
        batman.msg = ""
    else :
        LineBot_api.reply_message(event.reply_token, batman.msg_array)
        batman.msg_array = []
        batman.willImg = 0 

       

@handler.add (MessageEvent, message=LocationMessage)
def handle_Location_message (event):
    batman.trigger("position",event) 
    LineBot_api.reply_message(event.reply_token, TextSendMessage(text=batman.msg)) 
    batman.msg = ""

if __name__ == '__main__':        
    app.run(port=5002)