from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
from env import *
from machine import *


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
    LineBot_api.reply_message(event.reply_token, TextSendMessage(text=batman.msg)) 
    batman.msg = ""
    
    # if split_message[0] == "setdb":
    #     name = event.message.text.split(' ')[1] #name
    #     date = datetime.date(2022,int(event.message.text.split(' ')[2].split('/')[0]), int(event.message.text.split(' ')[2].split('/')[1]))  #data -> 12/04
    #     insert(name,date)
    #     msg = "insert"
    #     LineBot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    # elif split_message[0] == "cleardb":
    #     name = event.message.text.split(' ')[1]
    #     students.query.filter(students.name == name).delete()
    #     db.session.commit()
    #     msg = "delete success"
    #     LineBot_api.reply_message(event.reply_token, TextSendMessage(text=msg)) 
    # elif split_message[0] == "db":
    #     datas = students.query.all()
    #     msg="" 
    #     for student in datas:
    #         msg+=f"{student.name}, {student.date}, {student.live} \n"
    #     LineBot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    # elif split_message[0] == "help":
    #     msg = " ( 1 ) : setdb itemsName date \n ( 2 ) : cleardb itemsName \n ( 3 ) : db \n"
    #     LineBot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

    # elif split_message[0] == "game":
    #     global target
    #     msg = ""
    #     if split_message[1] == "new":
    #         target = int(random.random()*100)
    #         msg = "new target" 
    #     else:
    #         number = int(split_message[1])
    #         if(number > target):
    #             msg = "lower"
    #         elif (number < target) :
    #             msg = "higher"
    #         else:
    #             msg ="bingo"

    #     LineBot_api.reply_message(event.reply_token, TextSendMessage(text=msg)) 
    # else:
    #     LineBot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

# def printDB(self):
#         items = elevator.query.all()
#         msg="" 
#         for item in items:
#             msg+=f"{item.name}, {item.date} \n"
#         self.msg = msg
        
# def newItemDB(self,name,date):
#     date = datetime.date(2022,int(date.split('/')[0]), int(date.split('/')[1]))  #data -> 12/04
#     item = elevator(name,date)
#     db.session.add(item)
#     db.session.commit()
#     self.msg = "add" + str(name)
    
# def deleteItemDB(self,name):
#     elevator.query.filter(elevator.name == name).delete()
#     db.session.commit()
#     self.msg = "delete " + str(name) +" success"   

if __name__ == '__main__':        
    app.run(port=5002)