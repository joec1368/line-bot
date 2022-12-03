from transitions import Machine
from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DATE
from env import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = database_uri

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # inherit from this class to create ORM models
session = sessionmaker(engine)
db = session()

class elevator(Base):
    __tablename__ = 'elevators'
    sid = Column(Integer,primary_key = True)
    name = Column(String(200),nullable = False)
    date = Column(DATE)
    live = Column(Boolean)
    
    def __init__(self,name,date):
        self.name = name,
        self.date = date,
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =  database_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db=SQLAlchemy(app)



class bot(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['init', 'tutorial', 'elevator', 'playground','help_elevator','getDB','newDB','deleteDB']
    msg = ""
    target = 0
    



    def __init__(self, name):
        
        self.name = name

        self.machine = Machine(model=self, states=bot.states, initial='init')
        
        self.machine.add_transition(trigger='wake_up', source='asleep', dest='hanging out')
        
        self.machine.add_transition('help','init','tutorial')
        
        self.machine.add_transition('play',['init','tutorial'],'playground',before = 'random_number')
        
        self.machine.add_transition('guess','playground','=',before = 'guess')
        
        self.machine.add_transition('exit','*','init')
        
        self.machine.add_transition('elevator',['init','tutorial','help_elevator'],'elevator')
        
        self.machine.add_transition('db',['elevator','help_elevator','newDB','deleteDB'],'getDB',after = 'printDB')
        
        self.machine.add_transition('new',['elevator','help_elevator','getDB','deleteDB'],'newDB',after = 'newItemDB')
        
        self.machine.add_transition('delete',['elevator','help_elevator','newDB','getDB'],'deleteDB',after = 'deleteItemDB')
        
        self.machine.add_transition('db','getDB','=',before = 'printDB')
        
        self.machine.add_transition('new','newDB','=',before = 'newItemDB')
        
        self.machine.add_transition('delete','deleteDB','=',before = 'deleteItemDB')
        
        self.machine.add_transition('help', ['elevator','getDB','newItemDB','deleteItemDB'],'help_elevator')
               
        self.machine.on_enter_tutorial(self.print_info) 
        
        self.machine.on_enter_elevator(self.print_elevator)
        
        self.machine.on_enter_init(self.in_init)
        
        self.machine.on_enter_help_elevator(self.help_in_elevator)
        
    def in_init(self):
        self.msg = "hi it is robot !"
        
    def print_info(self):
        self.msg = "help in info"
        
    def random_number(self):
        self.target = int(random.random() * 100)
        self.msg = " Let's guess ! "
        
    def guess(self,number):
        number = int(number)
        if(number > self.target):
            self.msg = "lower"
        elif (number < self.target) :
            self.msg = "higher"
        else:
            self.msg ="bingo ! \n And I will change target number !"
            self.random_number()
            
    def print_elevator(self):
        self.msg = ''' 
            This is your elevator!! \n
            You can use [ help ] command to get help
            '''
    def help_in_elevator(self):
        self.msg = '''This is you help:
        (1) db : get your items in your elevator
        (2) new : put items in your elevator
        \t usage : new itemName date 
        \t example : new water 12/31
        (3) delete : delete items in your elevator
        \t usage : delete itemName
        \t example : delete water
        '''
        
    def printDB(self):
        items = db.query(elevator)
        msg="" 
        for item in items:
            msg+=f"{item.name}, {item.date} \n"
        self.msg = msg
        
    def newItemDB(self,name,date):
        date = datetime.date(2022,int(date.split('/')[0]), int(date.split('/')[1]))  #data -> 12/04
        item = elevator(name,date)
        db.add(item)
        db.commit()
        self.msg = "add " + str(name)
        
    def deleteItemDB(self,name):
        db.query(elevator).filter(elevator.name == name).delete()
        db.commit()
        self.msg = "delete " + str(name) +" success"
        
        
batman = bot("Batman")