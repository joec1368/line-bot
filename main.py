from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage,VideoSendMessage
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
from env import *
from machine import *
from geopy.geocoders import Nominatim




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

user = ""
target = 0

list = {}
LineBot_api = LineBotApi(linebotapi)
handler = WebhookHandler(linehandler)

db=SQLAlchemy(app)

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
    if(event.message.text == "video" ):
        if os.path.isfile("./static/video.mp4") and os.path.isfile("./static/preview.jpg"):
            print("send")
            LineBot_api.reply_message(event.reply_token,VideoSendMessage(
            original_content_url = ngrok_url + "/static/video.mp4", # 影片的網址，可以參考圖片的上傳方式
            preview_image_url= ngrok_url + "/static/preview.jpg" # 影片預覽的圖片
            ))
            return
        

    try:
        split_message = event.message.text.split(' ')
        if event.source.user_id in list.keys():
            target = list[event.source.user_id]
        else :
            list[event.source.user_id] = bot("Batman");
            target = list[event.source.user_id]
        if len(split_message) == 1:
            target.trigger(split_message[0]) 
        if len(split_message) == 2:
            target.trigger(split_message[0],split_message[1])
        if len(split_message) == 3:
            target.trigger(split_message[0],split_message[1],split_message[2]) 
    except:
        target.msg = "your type has some error, please check"
        
    #print(split_message[0])
    # batman.trigger(split_message[0])
    #print("next")
    #print(batman.msg)
    if(target.willImg == 0):
        if target.quickply == 0:
            LineBot_api.reply_message(event.reply_token, TextSendMessage(text=target.msg)) 
        elif target.quickply == 1:
            LineBot_api.reply_message(event.reply_token, TextSendMessage(text=target.msg,quick_reply = target.reply)) 
            target.quickply = 0
            target.reply = ''
        target.msg = ""
    else :
        LineBot_api.reply_message(event.reply_token, ImageSendMessage(target.msg_array)) 
        target.quickply = 0
        target.reply = ''
        target.msg = ""
        target.msg_array = []
        target.willImg = 0 

       

@handler.add (MessageEvent, message=LocationMessage)
def handle_Location_message (event):
    if event.source.user_id in list.keys():
        target = list[event.source.user_id]
    else :
        list[event.source.user_id] = bot("Batman");
        target = list[event.source.user_id]
    try:
        target.trigger("position",event) 
    except:
        target.msg = "your type has some error, please check"      
         
    if target.quickply == 0:
        LineBot_api.reply_message(event.reply_token, TextSendMessage(text=target.msg)) 
    elif target.quickply == 1:
        LineBot_api.reply_message(event.reply_token, TextSendMessage(text=target.msg,quick_reply = target.reply)) 
        target.quickply = 0
        target.reply = ''
    target.msg = ""

if __name__ == '__main__':    
    app.run(port=80)

